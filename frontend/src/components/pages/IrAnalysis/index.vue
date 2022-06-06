<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">IR Analysis</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <ir-input
                    :duct="duct"
                    @get-ir-info="getIrInfo"
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
                    :resampled-ir="resampledIr"
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

    </v-container>
</template>
<script>
import IrInput from './IrInput'
import IrResult from './IrResult'
export default{
    components:{
        IrInput,
        IrResult
    },
    data:() =>({
        splRate:0,
        channels:0,
        audioSrc:'',
        fileName:'',
        resultShown: false,

        resampledIr:[],
        acousticParameters:[],
        schroederVals:{},
        timestamp:[],
        filterVals:{},
        freqList:[],
        loading:false,
        filterType:'FIR',
        order:3001,
        unstableHz:[]
    }),
    props:['duct'],
    methods:{
        getIrInfo(args){
            [ this.splRate, this.channels, this.audioSrc, this.fileName ] = args;
            this.callDuct();
            this.resultShown = false;
            this.$nextTick(()=> (this.resultShown = true));
        },
        async callDuct(rawIrRequired=true){
            this.loading = true;
            if (rawIrRequired){
                [ this.resampledIr, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: 'analysis' });
            }
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
            this.loading = false;
        },
        async updateFilterPreview(args){
            this.filterType = args.filterType;
            this.order = Number(args.order);
            [this.filterVals, this.freqList, this.unstableHz] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                spl_rate: this.splRate,
                filter_type: this.filterType,
                order: this.order
            });
        },
        updateAnalysis(args) {
            this.filterType = args.filterType;
            this.order = Number(args.order);
            this.callDuct(false);
        },
    },
    mounted(){
        window.addEventListener('beforeunload', async () => {
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: 'analysis'});
            if(isKeyExists) await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'analysis' });
        });
    },
}
</script>
