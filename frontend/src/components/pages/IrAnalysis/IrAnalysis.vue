<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        color="#323232"
        dark
    >
        <v-card-title>Result / {{fileName}}</v-card-title>
        <v-card-text>
            <v-row>
                <v-col class="text-body-1">
                    Audio Player
                </v-col>
            </v-row>
            <iflb-audio-player 
                :src="audioSrc"
                :is-required="{
                    skipBackward:false,
                    skipForward:false,
                    downloadIcon:false,
                    playbackSpeedIcon:false
                }"
            />
        </v-card-text>
        <v-card-text>
            <chart-tabs
                :default-filter-type="defaultFilterType"
                :default-order="defaultOrder"
                :resampled-ir="resampledIr"
                :channels="channels"
                :spl-rate="splRate"
                :timestamp="timestamp"
                :schroeder-decibels="schroederDecibels"
                :power-per-freq="powerPerFreq"
                :freq="freq"
                :is-stable-obj="isStableObj"
                :duct-calling="ductCalling"
                @emit-filter-info="updateFilterChart"
                @update-analysis="updateAnalysis"
            />
        </v-card-text>
        <v-card-text>
            <acoustic-parameter-table-card 
                :acoustic-parameters="acousticParameters"
                :duct-calling="ductCalling"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import IflbAudioPlayer from '../../ui/IflbAudioPlayer.vue'
import ChartTabs from './ChartTabs.vue'
import AcousticParameterTableCard from './AcousticParameterTableCard'
export default{
    components:{
        IflbAudioPlayer,
        ChartTabs,
        AcousticParameterTableCard,
    },
    data:() => ({
        resampledIr:[],
        acousticParameters:[],
        schroederDecibels:{},
        timestamp:[],
        powerPerFreq:{},
        freq:{},
        ductCalling:false,
        defaultFilterType:'FIR',
        defaultOrder:3001,
        isStableObj:{}
    }),
    props:['duct','irArr','splRate','channels','audioSrc','fileName'],
    methods:{
        async callDuct(_filterType, _order, rawIrRequired){
            this.ductCalling = true;
            if (rawIrRequired == true){
                let irDict = {};
                [ irDict, this.timestamp ]  = await this.duct.call(this.duct.EVENT.RESAMPLE_IR_CHART_GET, { ir_arr: this.irArr });
                this.resampledIr = Object.values(irDict);
            }
            this.acousticParameters  = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels,
                filter_type: _filterType,
                order: _order
            });
            this.schroederDecibels  = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
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
