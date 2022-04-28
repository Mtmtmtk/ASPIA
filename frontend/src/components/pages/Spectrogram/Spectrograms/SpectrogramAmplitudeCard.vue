<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        v-resize="onResize"
    >
        <loading-overlay 
            :loading="loading"
        />
        <div ref="sampleChart"/>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import Plotly from 'plotly.js-dist-min'
export default{
    components:{ 
        LoadingOverlay
    },
    data:()=>({
        loading:false,
        mode:'decibel',
        absMinDB:10,
        absMaxDB:0,
        decibelRange:[-10,0]
    }),
    props:{
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
        applyRange(){
            this.decibelRange = [-1*this.absMinDB, -1*this.absMaxDB];
        },
        getCurrentStatus(val){
            if(val == 'drawing') this.loading = true;
            else if(val == 'finished') this.loading = false;
        },
        onResize(){
            if(this.cardWidth != this.$refs.sampleChart.clientWidth){
                this.cardWidth = this.$refs.sampleChart.clientWidth;
                if(this.$refs.sampleChart.classList.contains('js-plotly-plot')){
                    this.relayoutChart();
                }
            }
        },
        async createChartData(){
            const data = [{
                type: 'heatmap',
                x: this.timestamp,
                y: this.frequencies,
                z: this.zData,
                colorscale: 'Jet',
                colorbar: {
                    title: {
                        text: 'Amplitude',
                        side: 'right'
                    }
                },
                zmax: 0.1,
                zmin: 0
            }];
            const layout = {
                title: 'Spectrogram',
                autosize: false,
                width: this.cardWidth,
                height: 500,
                margin: {
                    l: 65,
                    r: 50,
                    b: 65,
                    t: 90,
                },
                xaxis: {
                    title: {
                        text: 'Time (sec)'
                    }
                },
                yaxis: {
                    title: {
                        text: 'Frequency (Hz)'
                    }
                },
            };
            Plotly.newPlot(this.$refs.sampleChart, data, layout);
        }
    },
    mounted(){
        this.createChartData();
    }
}
</script>

