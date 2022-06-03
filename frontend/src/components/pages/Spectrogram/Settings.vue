<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        v-resize="onResize"
    >
        <loading-overlay :loading="loading"/>
        <v-card-text>
            <v-row class="pt-0 mt-0">
                <v-col cols="6">
                    <v-card color="#E0E0E0" flat>
                        <v-select
                            v-model="selectedWindow"
                            prepend-inner-icon="mdi-sine-wave"
                            :items="windowTypes"
                            item-color="#26A69A"
                            label="Window Function"
                            color="#26A69A"
                            outlined
                            flat
                            @change="updateWindowPreview"
                        />
                        <vue-mathjax :formula="windowFormula" />
                        <div ref="plotlyChart" />
                    </v-card>
                </v-col>
                <v-col cols="6">
                    <v-card color="#E0E0E0" flat>
                        <v-text-field
                            v-model="overlap"
                            label="Overlapping Percentage (%)"
                            color="#26A69A"
                            type="number"
                            outlined
                            flat
                        />
                        <v-text-field
                            v-model="samplingPoints"
                            label="Sampling Points"
                            color="#26A69A"
                            type="number"
                            outlined
                            flat
                            @blur="updateWindowPreview"
                        />
                        <v-text-field
                            :value="44100"
                            label="Sampling Rate (Hz)"
                            color="#26A69A"
                            type="number"
                            outlined
                            flat
                            disabled
                        />
                        <v-text-field
                            :value="(samplingPoints/44100).toFixed(4)"
                            label="Time Resolution (s)"
                            color="#26A69A"
                            type="number"
                            outlined
                            flat
                            disabled
                        />
                        <v-text-field
                            :value="(44100/samplingPoints).toFixed(1)"
                            label="Frequency Resolution (Hz)"
                            color="#26A69A"
                            type="number"
                            outlined
                            flat
                            disabled
                        />
                        <v-card-actions>
                            <v-spacer/>
                            <v-btn
                                dark
                                color="#26A69A"
                                @click="updateSpectrogram"    
                            >Apply to Spectrogram
                            </v-btn>
                        </v-card-actions>
                    </v-card>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import { VueMathjax } from 'vue-mathjax'
import Plotly from 'plotly.js-dist-min'
export default {
    components:{ 
        LoadingOverlay,
        VueMathjax 
    },
    data: () => ({
        selectedWindow: 'Hamming',
        samplingPoints: 2048,
        overlap: 50,
        windowTypes: [
            'Hamming',
            'Hann',
            'Blackman',
            //'Blackman-Harris',
            //'Blackman-Nuttall',
            //'Gaussian',
        ],
        cardWidth: null
    }),
    props: {
        currentTab: {
            type: Number,
            default: 0
        },
        loading: {
            type: Boolean,
            default: false
        },
        windowVals: {
            type: Array,
            default: () => ([])
        }
    },
    computed: {
        windowFormula() {
            if(this.selectedWindow == 'Hamming')
                return '$${\\omega(t) = 0.54 - 0.46\\cos{2\\pi t}}$$'
            else if(this.selectedWindow == 'Hann')
                return '$${\\omega(t) = 0.5 - 0.5\\cos{2\\pi t}}$$'
            else if(this.selectedWindow == 'Blackman')
                return '$${\\omega(t) = 0.42 - 0.5\\cos{2\\pi t} + 0.05\\cos{4\\pi t}}$$'
            else return ''
        }
    },
    watch: {
        currentTab(){
            if(this.currentTab == 4) setTimeout(() => {  this.onResize(); },5); //nextTick doesn't work
        },
        windowVals(){ this.renderPlotly(); }
    },
    methods: {
        onResize(){
            const widthChanged = this.cardWidth !== this.$refs.plotlyChart.clientWidth ? true : false ;
            const isZero = this.$refs.plotlyChart.clientWidth === 0 ? true : false ;
            const plotlyRendered = this.$refs.plotlyChart.classList.contains('js-plotly-plot');
            if( widthChanged && !isZero && plotlyRendered ){
                this.cardWidth = this.$refs.plotlyChart.clientWidth;
                this.relayoutChart();
            }
        },
        renderPlotly(){
            if(this.windowVals.length != 0){
                const data = [{
                    y: this.windowVals,
                    type: 'scatter',
                    fill: 'tonexty',
                    line: { 
                        width: 2,
                        color: '#26A69A'
                    }
                }];
                const layout = {
                    autosize: false,
                    width: this.cardWidth,
                    height: 325,
                    margin: { l: 50, r: 15, t: 8, b: 40 },
                    xaxis: { title: { text: 'Sampling Point' } },
                    yaxis: { title: { text: 'Amplitude' } },
                    paper_bgcolor: '#E0E0E0'
                };
                Plotly.newPlot(this.$refs.plotlyChart, data, layout);
            }
        },
        relayoutChart() {
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
        updateWindowPreview(){ this.$emit('update-window-preview', [this.selectedWindow, parseInt(this.samplingPoints)]); },
        updateSpectrogram(){ 
            this.$emit('update-spectrogram', [this.selectedWindow, parseInt(this.samplingPoints), parseInt(this.overlap)]); 
        }
    },
    mounted(){
        this.cardWidth = this.$refs.plotlyChart.clientWidth;
        this.renderPlotly();
    },
}
</script>
