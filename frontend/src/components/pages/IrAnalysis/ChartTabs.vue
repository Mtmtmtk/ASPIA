<template>
    <div>
        <v-tabs
            background-color='#E0E0E0'
            color='#26A69A'
            light
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
                    :ductCalling='ductCalling'
                />
            </v-tab-item>
            <v-tab-item>
                <schroeder-curve
                    :schroederDB='schroederDB'
                    :timestamp='timestamp'
                    :ductCalling='ductCalling'
                />
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>
<script>
import RawIrChart from './RawIrChart.vue'
import SchroederCurve from './SchroederCurve.vue'
export default{
    components:{
        RawIrChart,
        SchroederCurve,
    },
    data:() =>({
        chartTab:null
    }),
    props:['reshapedIr','channels','splRate','timestamp','schroederDB','ductCalling'],
}
</script>
