<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        class="rounded-b-lg"
    >
        <loading-overlay 
            :loading="loading"
        />
        <v-card-text>
            <line-chart 
                :chart-data="chartData"
                :options="chartOptions"
            /> 
        </v-card-text>
    </v-card>
</template>
<script>
import LineChart from './Charts/LineChart.vue'
import LoadingOverlay from '@/components/ui/LoadingOverlay'
export default{
    components:{
        LineChart,
        LoadingOverlay
    },
    props:['resampledIr','channels','splRate','timestamp','ductCalling'],
    data:() => ({
        loading:true,
        chartData: { labels:[], datasets:[] },
        chartOptions: {
            maintainAspectRatio:false,
            animation:{ duration:0 },
            tooltips:{ enabled:false },
            scales:{
                xAxes:[{
                    scaleLabel: {
                        display:true,
                        labelString:'Time (s)'
                    }
                }],
                yAxes:[{
                    scaleLabel: {
                        display:true,
                        labelString:'Amplitude'
                    },
                    ticks:{
                        max:1.0,
                        min:-1.0
                    }
                }]
            },
        },
    }),
    computed:{
        channelName(){
            if(this.channels == 4) return ['channel_W','channel_Y','channel_Z','channel_X']
            else if(this.channels == 2) return ['channel_left', 'channel_right']
            else if(this.channels == 1) return ['channel_1']
            else return []
        }
    },
    methods:{
        renderChart(){
            console.log(this.resampledIr)
            if(this.resampledIr.length != 0){
                let _data = { labels:[], datasets:[] };
                _data.labels = this.timestamp;
                const colorPalette = ['#26A69A','#A64316','#A4A61E', '#6F37A6']
                for(let channelArr of this.resampledIr){
                    const _ind = this.resampledIr.indexOf(channelArr);
                    _data.datasets.push({
                        label: this.channelName[_ind],
                        data: this.resampledIr[_ind],
                        borderWidth:1,
                        fill:false,
                        lineTension:0,
                        borderColor: colorPalette[_ind],
                        pointRadius:0.01,
                    });
                } 
                this.chartData = _data;
                this.loading = false;
            }
        }
    },
    watch:{
        resampledIr(){
            this.renderChart();
        },
        ductCalling(){
            this.loading=this.ductCalling;
        }
    },
    mounted(){
        this.renderChart();
    }
}
</script>
