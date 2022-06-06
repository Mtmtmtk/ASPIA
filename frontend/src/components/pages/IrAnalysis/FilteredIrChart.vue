<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        class="rounded-b-lg"
        v-resize="onResize"
    >
        <loading-overlay :loading="loading"/>
        <v-card-text class="py-2 my-0">
            <v-row class="py-0 my-0">
                <v-col cols="12">
                    <v-select
                        v-model="selectedHz"
                        prepend-inner-icon="mdi-sine-wave"
                        :items="octaveBands"
                        :item-text="octaveBands.text"
                        :item-value="octaveBands.value"
                        item-color="#26A69A"
                        label="Octave Band"
                        color="#26A69A"
                        outlined
                        flat
                    />
                </v-col>
            </v-row>
            <div ref="plotlyChart" />
        </v-card-text>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import { octaveBands } from '../library.js'
import Plotly from 'plotly.js-dist-min'
export default{
    components:{ LoadingOverlay },
    data:() => ({
        selectedHz:'31.5',
        octaveBands,
        cardWidth: null
    }),
    props: {
        currentTab: {
            type: Number,
            default: 0
        },
        loading: {
            type: Boolean,
            default: true
        },
        timestamp: {
            type: Array,
            default: () => ([])
        },
        filteredIrs: {
            type: Object,
            default: () => ([])
        },
        channels:{
            type: Number,
            default: 0
        },
    },
    computed:{
        channelNames(){
            if(this.channels == 4) return ['channel_W','channel_Y','channel_Z','channel_X']
            else if(this.channels == 2) return ['channel_left', 'channel_right']
            else if(this.channels == 1) return ['channel_1']
            else return []
        }
    },
    watch:{
        filteredIrs(){
            this.renderPlotly();
        },
        selectedHz(){
            this.renderPlotly();
        },
        currentTab(){
            if(this.currentTab == 1) setTimeout(() => {  this.onResize(); }, 5); //nextTick doesn't work
        },
    },
    methods:{
        onResize(){
            if(this.cardWidth != this.$refs.plotlyChart.clientWidth && this.$refs.plotlyChart.clientWidth != 0){
                this.cardWidth = this.$refs.plotlyChart.clientWidth;
                if(this.$refs.plotlyChart.classList.contains('js-plotly-plot')){
                    this.relayoutChart();
                }
            }
        },
        renderPlotly(){
            console.log(this.filteredIrs[this.selectedHz]);
            if(Object.keys(this.filteredIrs).length != 0){
                let data = [];
                for(let _idx in this.filteredIrs[this.selectedHz]){
                    const plotlyChannelData = {
                        x: this.timestamp,
                        y: this.filteredIrs[this.selectedHz][_idx],
                        type: 'lines',
                        name: this.channelNames[_idx]  
                    }
                    data.push(plotlyChannelData);
                }
                const layout = {
                    autosize: false,
                    width: this.cardWidth,
                    height: 500,
                    margin: {
                        l: 65,
                        r: 20,
                        b: 65,
                        t: 20,
                    },
                    xaxis: {
                        title: { text: 'Time (sec)' }
                    },
                    yaxis: {
                        title: { text: 'Amplitude' },
                    },
                    legend: {
                        x: 1,
                        y: 1,
                        xanchor: 'right',
                        bgcolor:'#FFFFFF'
                    },
                    paper_bgcolor: '#E0E0E0'
                };
                Plotly.newPlot(this.$refs.plotlyChart, data, layout);
            }
        },
        relayoutChart(){
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
    },  
    mounted(){
        this.renderPlotly();
    },
}
</script>
