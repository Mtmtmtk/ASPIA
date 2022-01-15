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
                :reshapedIr='reshapedIr'
                :channels='channels'
                :splRate='splRate'
                :timestamp='timestamp'
                :schroederDB='schroederDB'
                :ductCalling='ductCalling'
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
        AcousticParameterTable
    },
    data:() => ({
        reshapedIr:[],
        acousticParameters:[],
        schroederDB:{},
        timestamp:[],
        ductCalling:false
    }),
    props:['duct','irArr','splRate','channels','audioURL','fileName'],
    methods:{
        async callDuct(){
            let irDict = {};
            this.ductCalling = true;
            [ irDict, this.timestamp ]  = await this.duct.call(this.duct.EVENT.RESAMPLE_IR_CHART_GET, { ir_arr: this.irArr });
            this.reshapedIr = Object.values(irDict);
            
            this.acousticParameters  = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels
            });
            this.schroederDB  = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
                ir_arr: this.irArr,
                spl_rate: this.splRate,
                channels: this.channels
            });
            this.ductCalling = false;
        }
    },
    watch:{
        irArr(){
            this.callDuct();
        },
    },
    mounted(){
        if(this.irArr.length != 0) this.callDuct();
    }
}
</script>
