<template>
    <v-card
        light
        flat
        tile
        color='#E0E0E0'
        class='rounded-b-lg'
    >
        <v-overlay
            absolute
            color='#E0E0E0'
            :value='loading'
        >
            <v-progress-circular
                indeterminate
                color='#26A69A'
                size='64'
            />
        </v-overlay>
        <v-card-text>
            <line-chart 
                :data='chartData'
                :options='chartOptions'
            /> 
        </v-card-text>
    </v-card>
</template>
<script>
import LineChart from './Charts/LineChart.vue'
export default{
    components:{
        LineChart
    },
    props:['reshapedIr','channels','splRate','timestamp','ductCalling'],
    data:() => ({
        loading:false,
        chartOptions: {
            maintainAspectRatio:false,
            animation:{
                duration:0
            },
            scales:{
                xAxes:[{
                    ticks:{
                        stepSize:0.10
                    },
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
            tooltips:{
                enabled:false
            }   
        },
        chartData: { labels:[], datasets:[] },
        signalPerChannel:[],
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
            if(this.reshapedIr.length != 0){
                let _data = { labels:[], datasets:[] };
                _data.labels = this.timestamp;
                const colorPalette = ['#26A69A','#A64316','#A4A61E', '#6F37A6']
                for(let channelArr of this.reshapedIr){
                    const _ind = this.reshapedIr.indexOf(channelArr);
                    _data.datasets.push({
                        label: this.channelName[_ind],
                        data: this.reshapedIr[_ind],
                        borderWidth:1,
                        fill:false,
                        lineTension:0,
                        borderColor: colorPalette[_ind],
                        pointRadius:0.01,
                    });
                } 
                this.chartData = _data;
                this.loading = false;
            }else{
                this.loading = true;
            }
        }
    },
    watch:{
        reshapedIr(){
            this.renderChart();
        },
        ductCalling(){
            if(this.ductCalling == true)this.loading=true;
        }
    },
    mounted(){
        this.renderChart();
    }
}
</script>
