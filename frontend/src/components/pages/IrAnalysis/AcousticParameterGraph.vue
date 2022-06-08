<template>
    <v-card
        light
        flat
        tile
        color="#E0E0E0"
        class="rounded-b-lg"
        v-resize="onResize"
    >
        <loading-overlay :loading="loading"/>
        <v-card-text class="py-2 my-0">
            <v-row class="py-0 my-0">
                <v-col cols="12">
                    <v-select
                        v-model="selectedParameter"
                        prepend-inner-icon="mdi-chart-bar"
                        :items="parameterItems"
                        item-color="#26A69A"
                        label="Acoustic Parameter"
                        color="#26A69A"
                        outlined
                        flat
                    />
                </v-col>
            </v-row>
            <div ref="plotlyChart" />
        </v-card-text>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import Plotly from 'plotly.js-dist-min'
export default{
    components: { LoadingOverlay },
    data:() => ({
        selectedParameter: 'Reverberation Time (RT60)',
        parameterItems: [
            'Reverberation Time (RT60)',
            'Early Decay Time (EDT)',   
            'Definition (D50)',         
            'Clarity (C50)',            
            'Clarity (C80)',            
            'Centre Time (Ts)',         
        ]     
    }),
    props: {
        loading: {
            type: Boolean,
            default: true
        },
        acousticParameters: {
            type: Array,
            default: () => ([])
        }
    },
    watch: {
        acousticParameters() {
            this.renderPlotly();
        },
        selectedParameter() {
            this.renderPlotly();
        },
        currentTab(){
            if(this.currentTab == 2) setTimeout(() => {  this.onResize(); }, 5); //nextTick doesn't work
        },
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
            if(this.acousticParameters.length != 0){
                const _idx = this.parameterItems.indexOf(this.selectedParameter);
                let paramObj = this.acousticParameters[_idx];
                delete paramObj.parameter 
                let paramArr = [];
                for (let key in paramObj) 
                    paramArr.push({ key: key + 'Hz' , val: paramObj[key]})

                const sortOrder = ['31.5', '63', '125', '250', '500', '1k', '2k', '4k', '8k', '16k'];
                paramArr = paramArr.sort(function(a,b){ return sortOrder.indexOf(a.key.replace('Hz', '')) - sortOrder.indexOf(b.key.replace('Hz', '')) });
                    
                let barchartData = {
                    x: paramArr.map(el => el.key),
                    y: paramArr.map(el => el.val),
                    type: 'bar',
                    marker: { color: '#26A69A' }
                };

                let xaxisTitle = '';
                if ([0, 1, 5].includes(_idx)) 
                    xaxisTitle = 'Seconds';
                else if([3, 4].includes(_idx))
                    xaxisTitle = 'Decibel';
                else if(_idx == 2)
                    xaxisTitle = 'Percentage'

                const yrange = [[1.8, 2.2], [1.0, 3.0], [0.3, 0.7], [-3.68, 3.68], [-5, 5], [0.06, 0.26]];

                const layout = {
                    autosize: false,
                    width: this.cardWidth,
                    height: 372,
                    margin: { l: 50, r: 15, t:0, b: 40 },
                    xaxis: { title: { text: 'Frequency' } },
                    yaxis: { title: { text: xaxisTitle } },
                    paper_bgcolor: '#E0E0E0',
                    shapes: [
                        {
                            type: 'line',
                            text: 'hgoe',
                            xref: 'paper',
                            yref: 'y',
                            x0: 0,
                            y0: yrange[_idx][0],
                            x1: 1,
                            y1: yrange[_idx][0],
                            line: {
                                color: 'red',
                                width: 2
                            }
                        },
                        {
                            type: 'line',
                            xref: 'paper',
                            yref: 'y',
                            x0: 0,
                            y0: yrange[_idx][1],
                            x1: 1,
                            y1: yrange[_idx][1],
                            line: {
                                color: 'red',
                                width: 2
                            }
                        },
                        {
                            type: 'line',
                            xref: 'paper',
                            yref: 'y',
                            x0: 0,
                            y0: yrange[_idx][1],
                            x1: 1,
                            y1: yrange[_idx][1],
                            line: {
                                color: 'red',
                                width: 2
                            }
                        }
                    ],
                    annotations: [
                        {
                            showarrow: true,
                            align: 'right',
                            x: '31.5Hz',
                            y: yrange[_idx][0],
                            xanchor: 'left',
                            yanchor: 'middle',
                            ay: 30,
                            text: 'Min value for typical concert hall (mid-frequencies)'
                        },
                        {
                            showarrow: true,
                            align: 'right',
                            x: '31.5Hz',
                            y: yrange[_idx][1],
                            xanchor: 'left',
                            yanchor: 'middle',
                            text: 'Max value for typical concert hall (mid-frequencies)'
                        },
                    ]
                };
                const data = [barchartData];
                Plotly.newPlot(this.$refs.plotlyChart, data, layout);
            }
        },
        relayoutChart(){
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
    },  
    mounted(){
        this.renderPlotly();
    },
}
</script>
