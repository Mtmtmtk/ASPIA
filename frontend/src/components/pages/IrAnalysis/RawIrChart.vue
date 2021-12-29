<template>
    <v-card
        light
        flat
        tile
        color='#E0E0E0'
    >
        <v-overlay
            absolute
            color='#FAFAFA'
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
                :options='sampleOptions'
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
    props:['reshapedIr','channels'],
    data:() => ({
        loading:true,
        sampleOptions: {
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
                    }
                }]
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
    watch:{
        reshapedIr(){
            let _data = { labels:[], datasets:[] };
            _data.labels = this.reshapedIr.time_stamp.map(function(el){ return Number(el.toFixed(2))});
            const colorPalette = ['#26A69A','#A64316','#A4A61E', '#6F37A6']
            
            for(let channel in this.reshapedIr){
                const _ind = Object.keys(this.reshapedIr).indexOf(channel)
                if(!['time_stamp'].includes(channel)){
                    _data.datasets.push({
                        label: this.channelName[_ind],
                        data: this.reshapedIr[channel],
                        borderWidth:3,
                        fill:false,
                        lineTension:0,
                        borderColor: colorPalette[_ind],
                        pointRadius:0.01,

                    });
                }
            }
            this.chartData = _data;
            console.log(this.chartData)
        }
    },
    beforeUpdate(){
        this.loading = false;
    }
}
</script>
