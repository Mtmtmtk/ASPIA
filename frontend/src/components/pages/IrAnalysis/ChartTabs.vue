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
            <v-tab>Filter Settings</v-tab>
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
            <v-tab-item>
                <filter-settings 
                    :reshapedIr='reshapedIr'
                    :defaultFilterType='defaultFilterType'
                    :defaultOrder='defaultOrder'
                    :powerPerFreq='powerPerFreq'
                    :freq='freq'
                    :isStableObj='isStableObj'
                    :ductCalling='ductCalling'
                    @emit-filter-info='emitFilterInfo'
                    @update-analysis='updateAnalysis'
                />
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>
<script>
import RawIrChart from './RawIrChart.vue'
import SchroederCurve from './SchroederCurve.vue'
import FilterSettings from './FilterSettings.vue'
export default{
    components:{
        RawIrChart,
        SchroederCurve,
        FilterSettings,
    },
    data:() =>({
        chartTab:null
    }),
    props:[
        'defaultFilterType',
        'defaultOrder',
        'reshapedIr',
        'channels',
        'splRate',
        'timestamp',
        'schroederDB',
        'powerPerFreq',
        'freq',
        'isStableObj',
        'ductCalling'
    ],
    methods:{
        emitFilterInfo(args){
            this.$emit('emit-filter-info', args);
        },
        updateAnalysis(args){
            this.$emit('update-analysis', args);
        }
    }
}
</script>
