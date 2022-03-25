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
            <v-row class="pt-0 mt-0">
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
                    <line-chart 
                        :chart-data="chartData"
                        :options="chartOptions"
                    /> 
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import LineChart from '@/components/ui/Charts/LineChart.vue'
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import { octaveBands } from '../library.js'
export default{
    components:{
        LineChart,
        LoadingOverlay
    },
    props:['schroederDecibels','timestamp','loading'],
    data:() => ({
        selectedHz:'31.5',
        octaveBands,
        chartData: { labels:[], datasets:[] },
        chartOptions: {
            maintainAspectRatio:false,
            animation:{ duration:0 },
            legend:{ display:false },
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
                        labelString:'dB'
                    }
                }]
            },
        },
    }),
    watch:{
        schroederDecibels(){
            this.updateChartData();
        },
        selectedHz(){
            this.updateChartData();
        },
    },
    methods:{
        updateChartData(){
            if(Object.keys(this.schroederDecibels).length != 0){
                let _data = { labels:[], datasets:[] };
                _data.labels = this.schroederDecibels.time_stamp.map(el => el.toFixed(2));
                const color = ['#26A69A','#B2DfD8']
                const _ind = this.octaveBands.map(el => el.value).indexOf(this.selectedHz);
                const _dataLabel = this.octaveBands.map(el => el.text)[_ind];
                _data.datasets.push({
                    label: _dataLabel,
                    data: this.schroederDecibels[this.selectedHz],
                    borderWidth:3,
                    fill:true,
                    lineTension:0.2,
                    borderColor: color[0],
                    backgroundColor:color[1],
                    pointRadius:0.01,

                });
                this.chartData = _data;
            }
        }
    },  
    mounted(){
        this.updateChartData();
    },
}
</script>
