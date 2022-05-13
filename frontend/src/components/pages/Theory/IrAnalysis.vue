<template>
    <v-card class="ma-0 pa-0 overflow-auto">
        <v-card-title>IR Analysis</v-card-title>
        <v-card-text class="text-body-1">
            <v-row><v-col>{{sentences[0] + " " + sentences[1]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[0]" />
            <v-row><v-col>{{sentences[2]}}</v-col></v-row>
            <v-img 
                class="mt-1"
                max-height="250"
                contain
                :src="images[0]"
            />
            <v-row class="pt-0 mt-0 text-center"><v-col>Fig.1. Schroeder Curve</v-col></v-row>
            <v-row><v-col>{{sentences[3]}}</v-col></v-row>
            <v-row class="pt-0 mt-0 text-center"><v-col>Table 1. Centre Frequency and its octave band[1]</v-col></v-row>
            <v-data-table 
                dense    
                :headers="octaveBandHeaders"
                :items="octaveBandItems"
                disable-sort
                hide-default-footer
            />
            <v-row class="pb-3"><v-col>{{sentences[4] + " " + sentences[5]}}</v-col></v-row>
            <acoustic-parameters-expansion-panels/>
        </v-card-text>
        <v-card-text>
            <v-row class="text-h6"><v-col>Reference</v-col></v-row>
            <v-row
                v-for="(ref, ind) in references"
                :key="ref"
                class="my-0 py-0"
            >
                <v-col>
                    {{"["+ Number(ind+1) + "] " + ref}}
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import { contents } from './TheoryContents.js'
import AcousticParametersExpansionPanels from './AcousticParametersExpansionPanels'
export default{
    components:{ 
        VueMathjax,
        AcousticParametersExpansionPanels
    },
    data:() => ({
        contents:contents,
        octaveBandHeaders:[
            {text:'Centre Frequency (Hz)',value:'nominal'},
            {text:'Lower Band Limit (Hz)',value:'min'},
            {text:'Upper Band Limit (Hz)',value:'max'},
        ],
        octaveBandItems:[
            {nominal:'31.5', min:'22',   max:'44'},
            {nominal:'63',   min:'44',   max:'88'},
            {nominal:'125',  min:'88',   max:'177'},
            {nominal:'250',  min:'177',  max:'355'},
            {nominal:'500',  min:'355',  max:'710'},
            {nominal:'1000', min:'710',  max:'1420'},
            {nominal:'2000', min:'1420', max:'2840'},
            {nominal:'4000', min:'2840', max:'5680'},
            {nominal:'8000', min:'5680', max:'11360'},
            {nominal:'16000',min:'11360',max:'22720'},
        ]
    }),
    computed:{
        sentences(){
            return this.contents.IrAnalysis.sentences
        },
        formulas(){
            return this.contents.IrAnalysis.formulas
        },
        images(){
            return this.contents.IrAnalysis.images
        },
        references(){
            return this.contents.IrAnalysis.references
        }
    },
}
</script>
