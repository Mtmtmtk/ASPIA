<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">IR Analysis</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <audio-input
                    :duct="duct"
                    group-key="analysis"
                    text="Choose an impulse response you want to analyse."
                    @send-audio-info="getIrInfo"
                    @emit-loading-error="showSnackbar"
                />
            </v-col>
        </v-row>
        <v-row v-if="resultShown">
            <v-col>
                <ir-result
                    v-if="resultShown"
                    :loading="loading"
                    :file-name="fileName"
                    :audio-src="audioSrc"
                    :ir-arr="irArr"
                    :filtered-irs="filteredIrs"
                    :channels="channels"
                    :timestamp="timestamp"
                    :schroeder-vals="schroederVals"
                    :filter-vals="filterVals"
                    :freq-list="freqList"
                    :unstable-hz="unstableHz"
                    :acoustic-parameters="acousticParameters"
                    @update-filter-preview="updateFilterPreview"
                    @update-analysis="updateAnalysis"
                />
            </v-col>
        </v-row>
        <error-snackbar
            :snackbar-model.sync="errorSnackbar"    
            snackbar-text="Error has occurred. Please reload the page."
            button-text="close"
        />
    </v-container>
</template>
<script>
import AudioInput from '@/components/ui/AudioInput'
import IrResult from './IrResult'
import ErrorSnackbar from '@/components/ui/Snackbar'
export default{
    components:{
        AudioInput,
        IrResult,
        ErrorSnackbar
    },
    data:() =>({
        splRate: 0,
        channels: 0,
        audioSrc: '',
        fileName: '',
        resultShown : false,
        errorSnackbar: false,

        irArr: [],
        acousticParameters: [],
        schroederVals: {},
        timestamp: [],
        filterVals: {},
        freqList: [],
        loading: false,
        filterType: 'FIR',
        order: 3001,
        unstableHz: [],
        filteredIrs: {}
    }),
    props: ['duct'],
    methods: {
        getIrInfo(args) {
            [ this.splRate, this.channels, this.audioSrc, this.fileName ] = args;
            this.callDuct();
            this.resultShown = true;
        },
        async callDuct(rawIrRequired = true) {
            this.loading = true;
            try {
                if (rawIrRequired)
                    [ this.irArr, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: 'analysis' });
                this.acousticParameters = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order
                });
                this.schroederVals = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order
                });
                [this.filterVals, this.freqList, this.unstableHz] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order
                });

                this.filteredIrs = await this.duct.call(this.duct.EVENT.FILTERED_SIGNAL_GET, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order
                });
                console.log(this.filteredIrs)
                this.loading = false;
            }catch {
                this.showSnackbar();
            }
        },
        async updateFilterPreview(args) {
            try {
                this.filterType = args.filterType;
                this.order = Number(args.order);
                [this.filterVals, this.freqList, this.unstableHz] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order
                });
            }catch {
                this.showSnackbar();
            }
        },
        updateAnalysis(args) {
            try {
                this.filterType = args.filterType;
                this.order = Number(args.order);
                this.callDuct(false);
            }catch {
                this.showSnackbar(); 
            }
        },
        showSnackbar() {
            this.errorSnackbar = true;
        }
    },
    mounted() {
        window.addEventListener('beforeunload', async () => {
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: 'analysis' });
            if(isKeyExists)     await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'analysis' });
        });
    },
}
</script>
