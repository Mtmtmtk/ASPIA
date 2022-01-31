<template>
    <v-card
        light
        flat
        tile
        color='#E0E0E0'
        class='rounded-b-lg'
    >
        <loading-overlay 
            :loading='loading'
        />
        <v-card-text>
            <v-row class='pt-0 mt-0'>
                <v-col cols='12'>
                    <v-select
                        v-model='selectedHz'
                        prepend-inner-icon='mdi-sine-wave'
                        :items='selectItems' 
                        :item-text='selectItems.text'
                        :item-value='selectItems.value'
                        item-color='#26A69A'
                        label='Octave Band'
                        color='#26A69A'
                        outlined
                        flat
                    />
                    <line-chart 
                        :chartData='chartData'
                        :options='chartOptions'
                    /> 
                </v-col>
            </v-row>
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
    props:['schroederDB','timestamp','ductCalling'],
    data:() => ({
        loading:true,
        selectedHz:'31.5',
        selectItems:[
            { text: '31.5 Hz', value:'31.5' },
            { text: '63 Hz', value:'63' },
            { text: '125 Hz', value:'125' },
            { text: '250 Hz', value:'250' },
            { text: '500 Hz', value:'500' },
            { text: '1 kHz', value:'1k' },
            { text: '2 kHz', value:'2k' },
            { text: '4 kHz', value:'4k' },
            { text: '8 kHz', value:'8k' },
            { text: '16 kHz', value:'16k' },
        ],
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
        schroederDB(){
            this.updateChartData();
        },
        selectedHz(){
            this.updateChartData();
        },
        ductCalling(){
            if(this.ductCalling == true)this.loading = true;
        }
    },
    methods:{
        updateChartData(){
            if(Object.keys(this.schroederDB).length != 0){
                let _data = { labels:[], datasets:[] };
                _data.labels = this.schroederDB.time_stamp.map(el => el.toFixed(2));
                const color = ['#26A69A','#B2DfD8']
                const _ind = this.selectItems.map(el => el.value).indexOf(this.selectedHz);
                const _dataLabel = this.selectItems.map(el => el.text)[_ind];
                _data.datasets.push({
                    label: _dataLabel,
                    data: this.schroederDB[this.selectedHz],
                    borderWidth:3,
                    fill:true,
                    lineTension:0.2,
                    borderColor: color[0],
                    backgroundColor:color[1],
                    pointRadius:0.01,

                });
                this.chartData = _data;
                this.loading = false;
            }
        }
    },  
    mounted(){
        this.updateChartData();
    },
}
</script>
