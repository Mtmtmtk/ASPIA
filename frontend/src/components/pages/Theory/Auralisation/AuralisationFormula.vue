<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>Formula</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences :sentences="sentences.slice(6,9)" />
            <vue-mathjax :formula="formulas[0]" />
            <theory-sentences is-html :sentences="sentences.slice(9,10)" />
            <theory-sentences is-html :sentences="sentences.slice(10,13)" />
            <theory-sentences is-html :sentences="sentences.slice(13,15)" />
            <vue-mathjax :formula="formulas[1]" />
            <theory-sentences is-html :sentences="sentences.slice(15,16)" />
            <v-stepper>
                <v-stepper-step step="1" complete complete-icon="mdi-numeric-1">
                    Execute FFT to the input and anechoic sound files
                </v-stepper-step>
                <v-stepper-step step="2" complete complete-icon="mdi-numeric-2">
                    Multiply them
                </v-stepper-step>
                <v-stepper-step step="3" complete complete-icon="mdi-numeric-3">
                    Execute inverse FFT to the multiplied signal
                </v-stepper-step>
            </v-stepper>
            <theory-sentences is-html :sentences="sentences.slice(16,18)" />
            <image-with-caption
                :per-row="2"
                :images="[images[0].src]"
                :captions="[images[0].caption]"
            />
            <reference-card/>
        </v-card-text>
    </v-card>
</template>
<script>
import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
//import AudioWithTitle from '../ui/AudioWithTitle.vue'
import ReferenceCard from './ReferenceCard'
import { VueMathjax } from 'vue-mathjax'
import { contents } from '../TheoryContents.js'
export default{
    components: { 
        ImageWithCaption,
        TheorySentences,
        VueMathjax,
        ReferenceCard
        //AudioWithTitle
    },
    data:() => ({
        contents,
    }),
    computed:{
        sentences() {
            return this.contents.Auralisation.sentences
        },
        images() {
            return this.contents.Auralisation.images
        },
        formulas(){
            return this.contents.Auralisation.formulas
        },
        audios() {
            return this.contents.Auralisation.audios
        }
    }, 
}
</script>
