<template>
    <v-card 
        rounded='lg'
        elevation='5' 
        color='#323232'
        dark
    >
        <v-card-title>Result / {{fileName}}</v-card-title>
        <v-card-text>
            <audio-player 
                :audioURL='audioURL'
            />
        </v-card-text>
        <v-card-text>
            <chart-tabs
                :defaultFilterType='defaultFilterType'
                :defaultOrder='defaultOrder'
                :reshapedIr='reshapedIr'
                :channels='channels'
                :splRate='splRate'
                :timestamp='timestamp'
                :schroederDB='schroederDB'
                :powerPerFreq='powerPerFreq'
                :freq='freq'
                :isStableObj='isStableObj'
                :ductCalling='ductCalling'
                @emit-filter-info='updateFilterChart'
                @update-analysis='updateAnalysis'
            />
        </v-card-text>
        <v-card-text>
            <acoustic-parameter-table 
                :acousticParameters='acousticParameters'
                :ductCalling='ductCalling'
            />
        </v-card-text>
    </v-card>
</template>
<script>
import AudioPlayer from './AudioPlayer.vue'
import ChartTabs from './ChartTabs.vue'
import AcousticParameterTable from './AcousticParameterTable.vue'
export default{
    components:{
        AudioPlayer,
        ChartTabs,
        AcousticParameterTable,
    },
    data:() => ({
        reshapedIr:[],
        acousticParameters:[],
        schroederDB:{},
        timestamp:[],
        powerPerFreq:{},
        freq:{},
        ductCalling:false,
        defaultFilterType:'FIR',
        defaultOrder:3001,
        isStableObj:{}
    }),
    props:['duct','irArr','splRate','channels','audioURL','fileName'],
    methods:{
        async callDuct(_filterType, _order, rawIrRequired){
            this.ductCalling = true;
            if (rawIrRequired == true){
                let irDict = {};
                [ irDict, this.timestamp ]  = await this.duct.call(this.duct.EVENT.RESAMPLE_IR_CHART_GET, { ir_arr: this.irArr });
                this.reshapedIr = Object.values(irDict);
                console.log(this.reshapedIr)    
            }
            this.acousticParameters  = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels,
                filter_type: _filterType,
                order: _order
            });
            this.schroederDB  = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels,
                filter_type: _filterType,
                order: _order
            });
            [this.powerPerFreq, this.freq, this.isStableObj]  = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                spl_rate: this.splRate,
                filter_type: _filterType,
                order: _order
            });
            console.log(this.freq)
            this.ductCalling = false;
        },
        async updateFilterChart(args){
            const _filterType = args.filterType;
            const _order = args.order;
            [this.powerPerFreq, this.freq, this.isStableObj]  = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                spl_rate: this.splRate,
                filter_type: _filterType,
                order: Number(_order)
            });
        },
        updateAnalysis(args){
            const _filterType = args.filterType;
            const _order = Number(args.order);
            this.callDuct(_filterType, _order, false);
        }
    },
    watch:{
        irArr(){
            this.callDuct(this.defaultFilterType,this.defaultOrder,true);
        },
    },
    mounted(){
        if(this.irArr.length != 0) this.callDuct(this.defaultFilterType,this.defaultOrder,true);
    }
}
</script>
