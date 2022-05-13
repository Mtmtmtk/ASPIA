<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        v-resize="onResize"
    >
        <loading-overlay :loading="loading"/>
        <v-card-text class="py-2 my-0">
            <plotly-setting-dialog 
                :mode="mode"
                :val-range="valRange"
                :time-range="timeRange"
                :frequency-range="frequencyRange"
                :color-scale="colorScale"
                @confirm-changes="updateChart"
            />
            <div ref="plotlyChart"/>
        </v-card-text>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import PlotlySettingDialog from './PlotlySettingDialog.vue'
import Plotly from 'plotly.js-dist-min'
export default{
    components:{ 
        LoadingOverlay,
        PlotlySettingDialog
    },
    data:()=>({
        valRange: [0, 0],
        timeRange: [0, 0],
        frequencyRange: [0, 22050],
        colorScale: 'Jet',
        cardWidth: null
    }),
    props:{
        loading: {
            type: Boolean,
            default: false
        },
        mode: {
            type: String,
            default: 'decibel'
        },
        initialValueRange: {
            type: Array,
            default: () => ([0, -10])
        },
        zData:{
            type: Array,
            default: () => ([])
        },
        timestamp: {
            type: Array,
            default: () => ([])
        },
        frequencies: {
            type: Array,
            default: () => ([])
        },
    },
    watch: {
        zData(){
            this.createChartData(); 
        }
    },
    methods:{
        onResize(){
            if(this.cardWidth != this.$refs.plotlyChart.clientWidth){
                this.cardWidth = this.$refs.plotlyChart.clientWidth;
                if(this.$refs.plotlyChart.classList.contains('js-plotly-plot')){
                    this.relayoutChart();
                }
            }
        },
        async createChartData() {
            let _text = '';
            if(this.mode == 'decibel') {
                _text = 'Decibel(dB)'
            }else if(this.mode == 'power') {
                _text = 'Power'
            }else if(this.mode == 'amplitude') {
                _text = 'Amplitude'
            }
            const data = [{
                type: 'heatmap',
                x: this.timestamp,
                y: this.frequencies,
                z: this.zData,
                colorscale: this.colorScale,
                colorbar: {
                    title: {
                        text: _text,
                        side: 'right'
                    }
                },
                zmax: this.valRange[1],
                zmin: this.valRange[0]
            }];
            const layout = {
                autosize: false,
                width: this.cardWidth,
                height: 406,
                margin: { l: 50, r: 0, t: 5, b: 60 },
                xaxis: { title: { text: 'Time (sec)' } },
                yaxis: { title: { text: 'Frequency (Hz)' } },
                paper_bgcolor: '#E0E0E0'
            };
            Plotly.newPlot(this.$refs.plotlyChart, data, layout);
        },
        relayoutChart() {
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
        updateChart(settings) {
            this.valRange = settings.valRange;
            this.timeRange = settings.timeRange;
            this.frequencyRange = settings.frequencyRange;
            this.colorScale = settings.colorScale;
            const styleUpdate = {
                zmax: this.valRange[1],
                zmin: this.valRange[0],
                colorscale: this.colorScale
            };
            const layoutUpdate = {
                xaxis: { range: this.timeRange },
                yaxis: { range: this.frequencyRange }
            }
            Plotly.restyle(this.$refs.plotlyChart, styleUpdate);
            Plotly.relayout(this.$refs.plotlyChart, layoutUpdate);
        }
    },
    mounted(){
        this.valRange = this.initialValueRange;
        this.timeRange = [0, this.timestamp[this.timestamp.length - 1]];
        this.createChartData();
    }
}
</script>

