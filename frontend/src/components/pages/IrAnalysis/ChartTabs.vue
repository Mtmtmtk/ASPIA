<template>
    <div>
        <tab-headers
            v-model="chartTab"
            :tab-header-info="tabHeaderInfo"
        />
        <v-tabs-items 
            v-model="chartTab"
            class="rounded-b-lg"
        >
            <v-tab-item>
                <ir-chart
                    :current-tab="chartTab"
                    :loading="loading"
                    :ir-arr="irArr"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <filtered-ir-chart 
                    :current-tab="chartTab"
                    :loading="loading"
                    :filtered-irs="filteredIrs"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <schroeder-curve
                    :current-tab="chartTab"
                    :loading="loading"
                    :schroeder-vals="schroederVals"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <acoustic-parameter-graph
                    :current-tab="chartTab"
                    :loading="loading"
                    :acoustic-parameters="acousticParameters"
                />
            </v-tab-item>
            <v-tab-item>
                <filter-settings 
                    :current-tab="chartTab"
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
import FilteredIrChart from './FilteredIrChart'
import SchroederCurve from './SchroederCurve'
import AcousticParameterGraph from './AcousticParameterGraph'
import FilterSettings from './FilterSettings'
import TabHeaders from './TabHeaders'
export default{
    components:{
        IrChart,
        FilteredIrChart,
        SchroederCurve,
        AcousticParameterGraph,
        FilterSettings,
        TabHeaders
    },
    data:() => ({
        chartTab:null,
        tabHeaderInfo: [
            {
                title: 'raw ir',
                tooltipHtml: '<span>Graph of the input impulse response.</span><br/><span>The graph is resampled into 4410 Hz to render faster  .</span>',
            },
            {
                title: 'filtered ir',
                tooltipHtml: '<span>Graphs of octave-band-filtered impulse responses.</span>'
            },
            {
                title: 'schroeder curve',
                tooltipHtml: '<span>Energy decay curves for the filtered impulse responses.</span><br/><span>Usage:</span><ul><li>Check remaining energy at time <i>t</i>.</li></ul>'    
            },
            {
                title: 'acoustic parameters',
                tooltipHtml: '<span>Acoustic parameters shown in graph format.</span><br/><span>Usage:</span><ul><li>Compare parameters with the typical value ranges of concert hall</li></ul>'
            },
            {
                title: 'filter settings',
                tooltipHtml: '<span>You can change the octave-band-filter settings applied in the analysis calculation.</span>'
            },
        ]
    }),
    props: {
        loading: {
            type: Boolean,
            default: true
        },
        irArr: {
            type: Array,
            default: () => ([])
        },
        filteredIrs: {
            type: Object,
            default: () => ({})
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
        acousticParameters: {
            type: Array,
            default: () => ([])
        },
    },
    methods:{
        onUpdateFilterPreview(args){ this.$emit('update-filter-preview', args); },
        onUpdateAnalysis(args){ this.$emit('update-analysis', args); }
    },
}
</script>
