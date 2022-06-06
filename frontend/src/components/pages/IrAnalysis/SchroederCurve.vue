<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        class="rounded-b-lg"
        v-resize="onResize"
    >
        <loading-overlay 
            :loading="loading"
        />
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
    components:{
        LoadingOverlay
    },
    props: {
        loading: {
            type: Boolean,
            default: true
        },
        timestamp: {
            type: Array,
            default: () => ([])
        },
        schroederVals: {
            type: Object,
            default: () => ({})
        },
    },
    data:() => ({
        selectedHz:'31.5',
        octaveBands,
        cardWidth: null
    }),
    watch:{
        schroederVals(){
            this.renderPlotly();
        },
        selectedHz(){
            this.renderPlotly();
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
            if(Object.keys(this.schroederVals).length != 0){
                const data = [{
                    x: this.timestamp,
                    y: this.schroederVals[this.selectedHz],
                    type: 'scatter',
                    fill: 'tonexty',
                    line: { 
                        width: 2,
                        color: '#26A69A'
                    },
                }];
                const layout = {
                    autosize: false,
                    width: this.cardWidth-2,
                    height: 372,
                    margin: { l: 50, r: 15, t: 8, b: 60 },
                    xaxis: { title: { text: 'Time (sec)'   } },
                    yaxis: { title: { text: 'Decibel (dB)' } },
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
