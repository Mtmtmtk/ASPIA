<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>How to analyse impulse response?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences :sentences="sentences.slice(14,16)" />
            <vue-mathjax :formula="formulas[3]"/>
            <theory-sentences 
                is-html
                :sentences="sentences.slice(16,20)" 
            />
            <octave-bands-table/>
            <theory-sentences :sentences="sentences.slice(20,22)" />
            <acoustic-parameters-expansion-panels />
            <reference-card/>
        </v-card-text>
    </v-card>
</template>
<script>
//import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import OctaveBandsTable from './OctaveBandsTable'
import AcousticParametersExpansionPanels from './AcousticParametersExpansionPanels'
import ReferenceCard from './ReferenceCard'
import { VueMathjax } from 'vue-mathjax'
import { contents } from '../TheoryContents.js'
export default {
    components: {
        //ImageWithCaption,  
        TheorySentences,
        OctaveBandsTable,
        AcousticParametersExpansionPanels,
        ReferenceCard,
        VueMathjax
    },
    data: () => ({
        contents
    }),
    computed:{
        sentences() {
            return this.contents.IrAnalysis.sentences
        },
        formulas() {
            return this.contents.IrAnalysis.formulas
        },
        images() {
            return this.contents.IrAnalysis.images
        }
    },
}
</script>
