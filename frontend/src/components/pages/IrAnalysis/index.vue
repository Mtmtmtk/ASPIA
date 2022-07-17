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
                    :html-text="true"
                    :duct="duct"
                    key-type="analysis"
                    :text="inputFormText"
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
            :snackbar-attrs="{
                timeout: -1,
                color: 'grey darken-3',
                multiLine: true
            }"
            :snackbar-model.sync="errorSnackbar"    
            snackbar-text="Error occurred. Please reload the page. Please email the developer (ms2676@york.ac.uk) if you get this message repeatedly."
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
        inputFormText: "Choose an impulse response you want to analyse. If you don't have any impulse responses, you can download it from <a href='https://www.openair.hosted.york.ac.uk/?page_id=36'>this link</a>.",

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
        maxRipple: 5,
        minAttenuation: 5,
        unstableHz: [],
        filteredIrs: {},
        redisKey: ''
    }),
    props: ['duct'],
    methods: {
        getIrInfo(args) {
            [ this.splRate, this.channels, this.audioSrc, this.fileName, this.redisKey ] = args;
            this.callDuct();
            this.resultShown = true;
        },
        async callDuct(rawIrRequired = true) {
            this.loading = true;
            try {
                if (rawIrRequired){
                    [ this.irArr, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: this.redisKey });
                    this.filteredIrs = await this.duct.call(this.duct.EVENT.FILTERED_SIGNAL_GET, {
                        group_key: this.redisKey,
                        spl_rate: this.splRate,
                        filter_type: this.filterType,
                        order: this.order,
                        ripple: this.maxRipple,
                        attenuation: this.minAttenuation
                    });
                    [this.filterVals, this.freqList, this.unstableHz] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                        spl_rate: this.splRate,
                        filter_type: this.filterType,
                        order: this.order,
                        ripple: this.maxRipple,
                        attenuation: this.minAttenuation
                    });
                }
                [ this.schroederVals, this.acousticParameters ] = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                    group_key: this.redisKey,
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order,
                    ripple: this.maxRipple,
                    attenuation: this.minAttenuation
                });
                this.loading=false;
                this.filteredIrs = await this.duct.call(this.duct.EVENT.FILTERED_SIGNAL_GET, {
                    group_key: this.redisKey,
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order,
                    ripple: this.maxRipple,
                    attenuation: this.minAttenuation
                });
            }catch {
                this.showSnackbar();
            }
        },
        async updateFilterPreview(args) {
            try {
                this.filterType = args.filterType;
                this.order = Number(args.order);
                this.maxRipple = Number(args.ripple);
                this.minAttenuation = Number(args.attenuation);
                [this.filterVals, this.freqList, this.unstableHz] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                    spl_rate: this.splRate,
                    filter_type: this.filterType,
                    order: this.order,
                    ripple: this.maxRipple,
                    attenuation: this.minAttenuation
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
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: this.redisKey });
            if(isKeyExists)     await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: this.redisKey });
        });
    },
}
</script>
