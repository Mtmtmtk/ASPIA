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
                    :loading="loading"
                    :audio-arr="resampledIr"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <schroeder-curve
                    :loading="loading"
                    :schroeder-vals="schroederVals"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <filter-settings 
                    :loading="loading"
                    :filter-vals="filterVals"
                    :freq-list="freqList"
                    :unstable-hz="unstableHz"
                    @update-filter-preview="onUpdateFilterPreview"
                    @update-analysis="onUpdateAnalysis"
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
    props: {
        loading: {
            type: Boolean,
            default: true
        },
        resampledIr: {
            type: Array,
            default: () => ([])
        },
        channels: {
            type: Number,
            default: 0
        },
        timestamp: {
            type: Array,
            default: () => ([])
        },
        schroederVals: {
            type: Object,
            default: () => ({})
        },
        filterVals: {
            type: Object,
            default: () => ({})
        },
        freqList: {
            type: Array,
            default: () => ([])
        },
        unstableHz: {
            type: Array,
            default: () => ([])
        },
    },
    methods:{
        onUpdateFilterPreview(args){ this.$emit('update-filter-preview', args); },
        onUpdateAnalysis(args){ this.$emit('update-analysis', args); }
    }
}
</script>
