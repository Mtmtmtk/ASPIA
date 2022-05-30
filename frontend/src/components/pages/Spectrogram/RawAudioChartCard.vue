<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        v-resize="onResize"
        height="500"
    >
        <loading-overlay :loading="loading"/>
        <div ref="plotlyChart" />
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import Plotly from 'plotly.js-dist-min'
export default{
    components:{ LoadingOverlay },
    data: () => ({
        cardWidth: null,
    }),
    props:{
        audioArr:{
            type: Array,
            default: ()=>([])
        },
        channels:{
            type: Number,
            default: 0
        },
        timestamp:{
            type:Array,
            default: ()=>([])
        },
        loading:{
            type:Boolean,
            default: false
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
            if(this.audioArr.length != 0){
                let data = [];
                for(let _idx in this.audioArr){
                    const plotlyChannelData = {
                        x: this.timestamp,
                        y: this.audioArr[_idx],
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
                        range: [-1, 1]
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
    watch:{
        audioArr(){
            this.renderPlotly();
        },
    },
    mounted(){
        this.renderPlotly();
    }
}
</script>
