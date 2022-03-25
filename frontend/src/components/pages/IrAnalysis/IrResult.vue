<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        color="#323232"
        dark
    >
        <v-card-title>Result / {{ fileName }}</v-card-title>
        <v-card-text>
            <v-row>
                <v-col class="text-body-1">
                    Audio Player
                </v-col>
            </v-row>
            <v-audio 
                :src="audioSrc"
                :display-flags="{
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
                :freq-list="freqList"
                :stability-check-obj="stabilityCheckObj"
                :duct-calling="ductCalling"
                @emit-filter-info="updateFilterChart"
                @update-analysis="updateAnalysis"
            />
        </v-card-text>
        <v-card-text>
            <acoustic-parameter-table-card 
                :acoustic-parameters="acousticParameters"
                :loading="ductCalling"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import VAudio from '@/components/ui/VAudio'
import ChartTabs from './ChartTabs'
import AcousticParameterTableCard from './AcousticParameterTableCard'
export default{
    components:{
        VAudio,
        ChartTabs,
        AcousticParameterTableCard,
    },
    data:() => ({
        resampledIr:[],
        acousticParameters:[],
        schroederDecibels:{},
        timestamp:[],
        powerPerFreq:{},
        freqList:{},
        ductCalling:false,
        defaultFilterType:'FIR',
        defaultOrder:3001,
        stabilityCheckObj:{}
    }),
    props:['duct','irArr','splRate','channels','audioSrc','fileName'],
    methods:{
        async callDuct(_filterType, _order, rawIrRequired){
            this.ductCalling = true;
            if (rawIrRequired == true){
                let irDict = {};
                [ irDict, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { arr: this.irArr });
                this.resampledIr = Object.values(irDict);
            }
            this.acousticParameters = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels,
                filter_type: _filterType,
                order: _order
            });
            this.schroederDecibels = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels,
                filter_type: _filterType,
                order: _order
            });
            [this.powerPerFreq, this.freqList, this.stabilityCheckObj] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
                spl_rate: this.splRate,
                filter_type: _filterType,
                order: _order
            });
            this.ductCalling = false;
        },
        async updateFilterChart(args){
            const _filterType = args.filterType;
            const _order = args.order;
            [this.powerPerFreq, this.freqList, this.stabilityCheckObj] = await this.duct.call(this.duct.EVENT.FILTER_SPECTRUM_GET, {
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
            this.callDuct(this.defaultFilterType, this.defaultOrder,true);
        },
    },
    mounted(){
        if(this.irArr.length != 0) this.callDuct(this.defaultFilterType, this.defaultOrder,true);
    }
}
</script>
