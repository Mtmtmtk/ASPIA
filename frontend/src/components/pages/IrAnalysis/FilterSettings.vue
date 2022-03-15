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
                <v-col cols="6">
                    <v-card color="#E0E0E0" flat>
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
                    </v-card>
                </v-col>
                <v-col cols='6'>
                    <v-card color='#E0E0E0' flat>
                        <v-text-field
                            v-model="filterOrder"
                            label="Filter Order"
                            outlined
                            type="number"
                            @blur="updateFilterChart"
                        />
                        <v-select
                            v-model="filterType"
                            prepend-inner-icon="mdi-filter"
                            :items="filterTypes"
                            label="Filter Type"
                            outlined
                            @change="updateFilterChart"
                        />
                        <v-alert
                            v-if="orderWaring"
                            dense
                            type="warning"
                        > The larger order might cause a long calculation time. Consider to make the order smaller.
                        </v-alert>
                        <v-alert
                            v-if="unstableFilter"
                            dense
                            type="error"
                        > The filter is unstable at {{ unstableHz }}. Please change the order or the type.
                        </v-alert>
                        <v-alert
                            v-if="invalidOrderError"
                            dense
                            type="error"
                        > The order of the FIR filter should be an odd number.
                        </v-alert>
                        <v-row>
                            <v-col cols="12" class="d-flex justify-end">
                                <v-btn 
                                    color="#26A69A"
                                    dark
                                    :disabled="buttonDisabled"
                                    @click="updateAnalysis"
                                >apply to analysis
                                </v-btn>
                            </v-col>
                        </v-row>
                    </v-card>
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
    data:() =>({
        orderWaring:false,
        invalidOrderError:false,
        unstableFilter:false,
        selectedHz:'31.5',
        octaveBands,
        chartOptions: {},
        chartData: { labels:[], datasets:[] },
        filterOrder:3001,
        filterType:'FIR',
        filterTypes:['Butterworth','Chebychev1','Chebychev2','Elliptic','Bessel','FIR'],
        buttonDisabled:false,
        unstableHz:''
    }),
    props:['resampledIr','defaultFilterType','defaultOrder','powerPerFreq','freqList','stabilityCheckObj','loading'],
    watch:{
        resampledIr(){
            this.filterOrder = this.defaultOrder;
            this.filterType = this.defaultFilterType;
        },
        powerPerFreq(){
            this.switchChartByOctave();
        },
        selectedHz(){
            this.switchChartByOctave()
        },
        stabilityCheckObj(){
            const unstableHzList = this.stabilityCheckObj.filter(el => el.isStable == false).map(el => el.hz);
            if(unstableHzList.length != 0){
                this.unstableFilter = true;
                this.buttonDisabled = true;
            }else{
                this.unstableFilter = false;
                this.buttonDisabled = false;
            }
            this.unstableHz = unstableHzList.join('Hz, ').concat('','Hz');
        },
        filterOrder(){
            if(this.filterOrder > 5000) this.orderWaring = true;
            else this.orderWaring = false;
        }
    },
    methods:{
        switchChartByOctave(){
            this.switchChartData();
            this.switchChartOptions();
        },
        switchChartData(){
            if(Object.keys(this.powerPerFreq).length != 0){
                let _data = { labels:[], datasets:[] };
                const color = ['#26A69A','#B2DfD8']
                const _idx = this.octaveBands.map(el => el.value).indexOf(this.selectedHz);
                const _dataLabel = this.octaveBands.map(el => el.text)[_idx];
                let _dataInDataset=[];
                for(let _idx=0; _idx < this.powerPerFreq[this.selectedHz].length; _idx++){
                    _dataInDataset.push({ x: Number(this.freqList[_idx].toFixed()), y: Number(this.powerPerFreq[this.selectedHz][_idx].toFixed(1)) });
                }
                _data.datasets.push({
                    label: _dataLabel,
                    data: _dataInDataset,
                    borderWidth:2,
                    fill:true,
                    lineTension:0.2,
                    borderColor: color[0],
                    pointRadius:0.01,
                });
                this.chartData = _data;
            }
        },
        switchChartOptions(){
            let _options = { 
                maintainAspectRatio:false,
                animation:{ duration:0 },
                legend:{ display:false },
                scales:{
                    xAxes:[{
                        scaleLabel: { display:true, labelString:'Frequency (Hz)' },
                        type:'logarithmic',
                        ticks:{ callback:(val)=>(val) }
                    }],
                    yAxes:[{ scaleLabel: { display:true, labelString:'Gain (dB)' } }]
                },
                tooltips:{
                    callbacks:{ label: (tooltipItem) => (tooltipItem.xLabel + 'Hz: ' + tooltipItem.yLabel + 'dB' ) }
                }
            };
            const rangeToOneKHertz = ['31.5','63','125','250','500'];
            const rangeToNyq = ['1k','2k','4k','8k','16k'];
            if(rangeToOneKHertz.includes(this.selectedHz)) _options.scales.xAxes[0].ticks['max'] = 1000;
            else if(rangeToNyq.includes(this.selectedHz))  _options.scales.xAxes[0].ticks['max'] = 22050;
            this.chartOptions = _options;
        },
        updateFilterChart(){
            if(this.filterType == 'FIR' && this.filterOrder%2 == 0){
                this.invalidOrderError = true;
                this.buttonDisabled = true;
            }else if(this.filterType != 'FIR' && this.filterOrder > 10){
                this.orderWaring = true;
                this.buttonDisabled = true;
            }else{
                this.$emit('emit-filter-info', { 
                    order: this.filterOrder, 
                    filterType: this.filterType
                });
                this.invalidOrderError = false;
            }
        },
        updateAnalysis(){
            this.$emit('update-analysis', { 
                order: this.filterOrder, 
                filterType: this.filterType
            });
        }
    },  
    mounted(){
        this.switchChartByOctave();
    },
}
</script>
