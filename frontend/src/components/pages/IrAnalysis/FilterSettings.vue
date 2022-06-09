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
        <v-card-text>
            <v-row class="pb-0 pt-1">
                <v-col cols="6" class="pb-0">
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
                            @change="renderPlotly"
                        />
                        <div ref="plotlyChart" />
                    </v-card>
                </v-col>
                <v-col cols="6" class="pb-0">
                    <v-card color='#E0E0E0' flat>
                        <v-text-field
                            v-model="filterOrder"
                            label="Filter Order"
                            outlined
                            type="number"
                            @blur="updateFitlerPreview"
                        />
                        <v-select
                            v-model="filterType"
                            prepend-inner-icon="mdi-filter"
                            :items="filterTypes"
                            label="Filter Type"
                            outlined
                            @change="updateFitlerPreview"
                        />
                        <v-text-field
                            v-if="['Chebychev1', 'Elliptic'].includes(filterType)"
                            v-model="maxRipple"
                            label="Max ripple in dB allowed below unity gain in the passband"
                            outlined
                            type="number"
                            @blur="updateFitlerPreview"
                        />
                        <v-text-field
                            v-if="['Chebychev2', 'Elliptic'].includes(filterType)"
                            v-model="minAttenuation"
                            label="Minimum attenuation required in the stop band"
                            outlined
                            type="number"
                            @blur="updateFitlerPreview"
                        />
                        <v-alert
                            v-if="rippleWaring"
                            dense
                            type="warning"
                        > The ripple value must be positive.
                        </v-alert>
                        <v-alert
                            v-if="attenuationWaring"
                            dense
                            type="warning"
                        > The attenuation value must be positive.
                        </v-alert>
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
                        > The filter is unstable at {{ unstableHzStr }}. Please change the order or the type.
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
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import { octaveBands } from '../library.js'
import Plotly from 'plotly.js-dist-min'
export default{
    components:{ LoadingOverlay },
    data:() =>({
        orderWaring: false,
        invalidOrderError: false,
        unstableFilter:false,
        rippleWaring: false,
        attenuationWaring: false,
        selectedHz: '31.5',
        octaveBands,
        filterOrder: 3001,
        filterType: 'FIR',
        filterTypes: ['Butterworth','Chebychev1','Chebychev2','Elliptic','Bessel','FIR'],
        buttonDisabled: false,
        unstableHzStr: '',
        maxRipple: 5,
        minAttenuation: 5
    }),
    props: {
        currentTab: {
            type: Number,
            default: 0
        },
        loading: {
            type: Boolean,
            default: true
        },
        filterVals: {
            type: Object,
            default: () => ({})
        },
        freqList: {
            type: Array,
            default: () => ([])
        },
        unstableHz: {
            type: Array,
            default: () => ([])
        },
    },
    watch:{
        unstableHz(){
            const unstableHzList = this.unstableHz.filter(el => el.isStable == false).map(el => el.hz);
            if(unstableHzList.length != 0){
                this.unstableFilter = true;
                this.buttonDisabled = true;
            }else{
                this.unstableFilter = false;
                this.buttonDisabled = false;
            }
            this.unstableHzStr = unstableHzList.join('Hz, ').concat('','Hz');
        },
        filterOrder(){
            if(this.filterOrder > 5000) this.orderWaring = true;
            else this.orderWaring = false;
        },
        filterVals() {
            this.renderPlotly();
        },
        currentTab(){
            if(this.currentTab == 3) setTimeout(() => {  this.onResize(); }, 5 ); //nextTick doesn't work
        }
    },
    methods:{
        onResize(){
            if(this.cardWidth != this.$refs.plotlyChart.clientWidth && this.$refs.plotlyChart.clientWidth != 0){
                this.cardWidth = this.$refs.plotlyChart.clientWidth;
                if(this.$refs.plotlyChart.classList.contains('js-plotly-plot'))
                    this.relayoutChart();
            }
        },
        renderPlotly(){
            if(Object.keys(this.filterVals).length != 0){
                let _HzRange = [];
                if(['31.5', '63', '125', '250'].includes(this.selectedHz))
                    _HzRange = [0, 3];//in expotensial form
                else
                    _HzRange = [2, 4.345];

                const data = [{
                    x: this.freqList,
                    y: this.filterVals[this.selectedHz],
                    type: 'scatter',
                    fill: 'tonexty',
                    line: { 
                        width: 2,
                        color: '#26A69A'
                    }
                }];
                const layout = {
                    autosize: false,
                    width: this.cardWidth,
                    height: 372,
                    margin: { l: 50, r: 15, t: 8, b: 60 },
                    xaxis: {
                        title: { text: 'Frequency (Hz)' },
                        type: 'log',
                        range: _HzRange
                    },
                    yaxis: { title: { text: 'Gain (dB)' } },
                    paper_bgcolor: '#E0E0E0'
                };
                Plotly.newPlot(this.$refs.plotlyChart, data, layout);
            }
        },
        relayoutChart(){
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.plotlyChart, update);
        },
        updateFitlerPreview(){
            if(this.filterType == 'FIR' && this.filterOrder % 2 == 0){
                this.invalidOrderError = true;
                this.buttonDisabled = true;
            }else if(this.filterType != 'FIR' && this.filterOrder > 10){
                this.orderWaring = true;
                this.buttonDisabled = true;
            }else if(this.maxRipple < 0 || this.maxRipple == ''){
                this.rippleWaring = true;
                this.buttonDisabled = true;
            }else if(this.minAttenuation < 0 || this.minAttenuation == ''){
                this.attenuationWaring = true;
                this.buttonDisabled = true;
            }else{
                this.$emit('update-filter-preview', { 
                    order: this.filterOrder, 
                    filterType: this.filterType,
                    ripple: this.maxRipple,
                    attenuation: this.minAttenuation
                });
                this.invalidOrderError = false;
            }
        },
        updateAnalysis(){
            this.$emit('update-analysis', { order: this.filterOrder, filterType: this.filterType });
        }
    },  
    mounted(){
        this.renderPlotly();
    },
}
</script>
