<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>Formula</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences 
                :sentences="sentences.slice(2,4)"
            />
            <vue-mathjax :formula="formulas[0]"/>
            <theory-sentences 
                :is-html="true" 
                :sentences="sentences.slice(4,7)"
            />
            <theory-sentences 
                row-class="mt-0 mb-1"
                :sentences="sentences.slice(7,9)"
            />

            <v-expansion-panels>
                <v-expansion-panel>
                    <v-expansion-panel-header color="#323232">Calculation Example</v-expansion-panel-header>
                    <v-expansion-panel-content color="#323232">
                        <theory-sentences :sentences="sentences[9]"/>
                        <vue-mathjax :formula="formulas[1]"/>
                        <vue-mathjax :formula="formulas[2]"/>
                        <theory-sentences :sentences="sentences[10]"/>
                        <vue-mathjax :formula="formulas[3]"/>
                        <theory-sentences :sentences="sentences.slice(11,13)"/>
                        <vue-mathjax :formula="formulas[4]"/>
                        <theory-sentences :sentences="sentences[13]"/>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>

            <theory-sentences 
                row-class="mt-1"
                :sentences="sentences.slice(14,18)"
            />
            <vue-mathjax :formula="formulas[5]"/>
            <theory-sentences :sentences="sentences.slice(18,20)"/>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import TheorySentences from '../ui/TheorySentences'
import { contents } from '../TheoryContents.js'
export default{
    components: { 
        VueMathjax,
        TheorySentences
    },
    data:() => ({
        contents,
    }),
    computed:{
        sentences() {
            return this.contents.Fourier.sentences
        },
        formulas() {
            return this.contents.Fourier.formulas
        },
        images() {
            return this.contents.Fourier.images
        }
    },
}
</script>
