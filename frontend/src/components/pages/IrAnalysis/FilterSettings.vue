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
                            <v-col cols="6">
                            </v-col>
                            <v-col cols="6" class="d-flex justify-end">
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
import LineChart from './Charts/LineChart.vue'
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import { octaveBands } from '../library.js'
export default{
    components:{
        LineChart,
        LoadingOverlay
    },
    data:() =>({
        //loading:true,
        loading:false,
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
    props:['reshapedIr','defaultFilterType','defaultOrder','powerPerFreq','freq','isStableObj','ductCalling'],
    watch:{
        reshapedIr(){
            this.filterOrder = this.defaultOrder;
            this.filterType = this.defaultFilterType;
        },
        powerPerFreq(){
            this.switchChartByOctave();
        },
        selectedHz(){
            this.switchChartByOctave()
        },
        ductCalling(){
            this.loading = this.ductCalling     
        },
        isStableObj(){
            let unstableHzList = [];
            const _boolList = Object.values(this.isStableObj);
            const _HzList = Object.keys(this.isStableObj);
            if(_boolList.includes(false)){
                for(let _ind=0; _ind < _HzList.length; _ind++){
                    if(_boolList[_ind] == false) unstableHzList.push(_HzList[_ind]);
                }
                this.unstableFilter = true;
                this.buttonDisabled = true;
            }else{
                this.unstableFilter = false;
                this.buttonDisabled = false;
            }
            this.unstableHz = unstableHzList.join('Hz, ');
            this.unstableHz = this.unstableHz.concat('','Hz');
        },
        filterOrder(){
            if(this.filterOrder > 5000) this.orderWaring = true;
            else this.orderWaring = false;
        }
    },
    methods:{
        switchChartByOctave(){
            this.switchChartByOctaveData();
            this.switchChartByOctaveOptions();
        },
        switchChartByOctaveData(){
            if(Object.keys(this.powerPerFreq).length != 0){
                let _data = { labels:[], datasets:[] };
                const color = ['#26A69A','#B2DfD8']
                const _ind = this.octaveBands.map(el => el.value).indexOf(this.selectedHz);
                const _dataLabel = this.octaveBands.map(el => el.text)[_ind];
                let _dataInDataset=[];
                for(let _ind=0; _ind < this.powerPerFreq[this.selectedHz].length; _ind++){
                    _dataInDataset.push({ x: Number(this.freq[_ind].toFixed()), y: Number(this.powerPerFreq[this.selectedHz][_ind].toFixed(1)) });
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
        switchChartByOctaveOptions(){
            let _options = { 
                maintainAspectRatio:false,
                animation:{ duration:0 },
                legend:{ display:false },
                scales:{
                    xAxes:[{
                        scaleLabel: {
                            display:true,
                            labelString:'Frequency (Hz)'
                        },
                        type:'logarithmic',
                        ticks:{ callback:(val)=>(val) }
                    }],
                    yAxes:[{
                        scaleLabel: {
                            display:true,
                            labelString:'Gain (dB)'
                        }
                    }]
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
