<template>
    <v-card 
        rounded='lg'
        elevation='5' 
        color='#323232'
    >
        <v-card-text>
            <v-tabs
                background-color='#E0E0E0'
                color='#26A69A'
                v-model='chartTab'
                class='rounded-t-lg'
            >
                <v-tab>raw ir</v-tab>
                <v-tab>schroeder curve</v-tab>
            </v-tabs>
            <v-tabs-items 
                v-model='chartTab'
                class='rounded-b-lg'
            >
                <v-tab-item>
                    <raw-ir-chart 
                        :reshapedIr='reshapedIr'
                        :channels='channels'
                        :splRate='splRate'
                        :timestamp='timestamp'
                    />
                </v-tab-item>
                <v-tab-item>
                    <schroeder-curve
                        :schroederDB='schroederDB'
                        :timestamp='timestamp'
                    />
                </v-tab-item>
            </v-tabs-items>
        </v-card-text>
        <v-card-text>
            <acoustic-parameter-table 
                :acousticParameters='acousticParameters'
            />
        </v-card-text>
    </v-card>
</template>
<script>
import RawIrChart from './RawIrChart.vue'
import SchroederCurve from './SchroederCurve.vue'
import AcousticParameterTable from './AcousticParameterTable.vue'
export default{
    components:{
        RawIrChart,
        SchroederCurve,
        AcousticParameterTable
    },
    data:() => ({
        chartTab:null,
        reshapedIr:[],
        acousticParameters:[],
        schroederDB:{}
    }),
    props:['duct','irArr','splRate','channels','timestamp'],
    watch:{
    },
    async mounted(){
        this.reshapedIr = this.irArr;
        
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
        console.log(this.schroederDB)
    }
}
</script>
