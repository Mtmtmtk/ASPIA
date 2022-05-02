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
            <v-row class="py-0 my-0">
                <v-col cols="5" class="pb-0">
                    <v-text-field 
                        outlined
                        dense
                        flat
                        label="minimum decibel"
                    />
                </v-col>
                <v-col cols="5" class="pb-0">
                    <v-text-field 
                        outlined
                        dense
                        flat
                        label="max decibel"
                    />
                </v-col>
                <v-col cols="2" class="pb-0">
                    <v-btn
                        color="#26A69A"
                        dark
                    >confirm
                    </v-btn>
                </v-col>
            </v-row>
            <div ref="plotlyChart"/>
        </v-card-text>
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
        decibelRange:[-10,0],
        cardWidth: null
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
            if(this.cardWidth != this.$refs.plotlyChart.clientWidth){
                this.cardWidth = this.$refs.plotlyChart.clientWidth;
                if(this.$refs.plotlyChart.classList.contains('js-plotly-plot')){
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
                        text: 'Decibel (dB)',
                        side: 'right'
                    }
                },
                zmax: 0,
                zmin: -10
            }];
            const layout = {
                autosize: false,
                width: this.cardWidth,
                height: 406,
                margin: {
                    l: 50,
                    r: 15,
                    t: 8,
                    b: 60
                },
                xaxis: {
                    title: { text: 'Time (sec)' }
                },
                yaxis: {
                    title: { text: 'Frequency (Hz)' },
                },
                paper_bgcolor: '#E0E0E0'
            };
            Plotly.newPlot(this.$refs.plotlyChart, data, layout);
        },
        relayoutChart(){
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
    },
    mounted(){
        this.createChartData();
    }
}
</script>

