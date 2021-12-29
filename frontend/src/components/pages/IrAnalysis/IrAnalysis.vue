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
            >
                <v-tab>raw ir</v-tab>
                <v-tab>Energy</v-tab>
            </v-tabs>
            <v-tabs-items v-model='chartTab'>
                <v-tab-item>
                    <raw-ir-chart 
                        :reshapedIr='reshapedIr'
                        :channels='channels'
                    />
                </v-tab-item>
                <v-tab-item>
                    <p>Test</p>
                </v-tab-item>
            </v-tabs-items>
        </v-card-text>
    </v-card>
</template>
<script>
import RawIrChart from './RawIrChart.vue'
export default{
    components:{
        RawIrChart
    },
    data:() => ({
        chartTab:null,
        reshapedIr:{}
    }),
    props:['duct','irArr','splRate','channels'],
    async mounted(){
        this.reshapedIr = await this.duct.call(this.duct.EVENT.RESHAPED_IR_GET, {
            ir_arr: this.irArr,
            spl_rate: this.splRate,
            channels: this.channels
        });
    }
}
</script>
