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
                :loading="loading"
                :resampled-ir="resampledIr"
                :channels="channels"
                :timestamp="timestamp"
                :schroeder-vals="schroederVals"
                :filter-vals="filterVals"
                :freq-list="freqList"
                :unstable-hz="unstableHz"
                @update-filter-preview="onUpdateFilterPreview"
                @update-analysis="onUpdateAnalysis"
            />
        </v-card-text>
        <v-card-text>
            <acoustic-parameter-table-card 
                :loading="loading"
                :acoustic-parameters="acousticParameters"
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
    props: {
        loading: {
            type: Boolean,
            default: true
        },
        fileName: {
            type: String,
            default: ''
        },
        audioSrc: {
            type: String,
            default: ''
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
        acousticParameters: {
            type: Array,
            default: () => ([])
        }
    },
    methods:{
        onUpdateAnalysis(args) { this.$emit('update-analysis', args); },
        onUpdateFilterPreview(args) { this.$emit('update-filter-preview', args); }
    },
}
</script>
