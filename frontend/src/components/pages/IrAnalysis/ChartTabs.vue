<template>
    <div>
        <v-tabs
            background-color="#E0E0E0"
            color="#26A69A"
            light
            v-model="chartTab"
            class="rounded-t-lg"
        >
            <v-tab>raw ir</v-tab>
            <v-tab>schroeder curve</v-tab>
            <v-tab>Filter Settings</v-tab>
        </v-tabs>
        <v-tabs-items 
            v-model="chartTab"
            class="rounded-b-lg"
        >
            <v-tab-item>
                <ir-chart
                    :audio-arr="resampledIr"
                    :channels="channels"
                    :timestamp="timestamp"
                    :loading="ductCalling"
                />
            </v-tab-item>
            <v-tab-item>
                <schroeder-curve
                    :schroeder-decibels="schroederDecibels"
                    :timestamp="timestamp"
                    :loading="ductCalling"
                />
            </v-tab-item>
            <v-tab-item>
                <filter-settings 
                    :resampled-ir="resampledIr"
                    :default-filter-type="defaultFilterType"
                    :default-order="defaultOrder"
                    :power-per-freq="powerPerFreq"
                    :freq-list="freqList"
                    :stability-check-obj="stabilityCheckObj"
                    :loading="ductCalling"
                    @emit-filter-info="emitFilterInfo"
                    @update-analysis="updateAnalysis"
                />
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>
<script>
import IrChart from './IrChart'
import SchroederCurve from './SchroederCurve'
import FilterSettings from './FilterSettings'
export default{
    components:{
        IrChart,
        SchroederCurve,
        FilterSettings,
    },
    data:() =>({
        chartTab:null
    }),
    props:[
        'defaultFilterType',
        'defaultOrder',
        'resampledIr',
        'channels',
        'splRate',
        'timestamp',
        'schroederDecibels',
        'powerPerFreq',
        'freqList',
        'stabilityCheckObj',
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
