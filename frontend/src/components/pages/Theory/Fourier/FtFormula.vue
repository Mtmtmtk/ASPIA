<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>Formula</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences 
                :sentences="sentences.slice(4,6)"
            />
            <vue-mathjax :formula="formulas[0]"/>
            <theory-sentences 
                :is-html="true" 
                :sentences="sentences.slice(6,9)"
            />
            <theory-sentences 
                row-class="mt-0 mb-1"
                :sentences="sentences.slice(9,11)"
            />

            <v-expansion-panels>
                <v-expansion-panel>
                    <v-expansion-panel-header color="#323232">Calculation Example 1: 440 Hz sine wave</v-expansion-panel-header>
                    <v-expansion-panel-content color="#323232">
                        <theory-sentences :sentences="sentences[11]"/>
                        <vue-mathjax :formula="formulas[1]"/>
                        <vue-mathjax :formula="formulas[2]"/>
                        <theory-sentences :sentences="sentences[12]"/>
                        <vue-mathjax :formula="formulas[3]"/>
                        <theory-sentences :sentences="sentences.slice(13,15)"/>
                        <vue-mathjax :formula="formulas[4]"/>
                        <theory-sentences :sentences="sentences[15]"/>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>

            <theory-sentences 
                row-class="my-1"
                :sentences="sentences.slice(16,17)"
            />

            <v-expansion-panels>
                <v-expansion-panel>
                    <v-expansion-panel-header color="#323232">Calculation Example 2: Square wave</v-expansion-panel-header>
                    <v-expansion-panel-content color="#323232">
                        <theory-sentences :sentences="sentences.slice(17,19)"/>
                        <audio-with-title
                            background-color="#323232"
                            :title="audios[0].title"
                            :src="audios[0].src"
                        />
                        <br>
                        <theory-sentences :sentences="sentences.slice(19,21)"/>
                        <vue-mathjax :formula="formulas[5]"/>
                        <image-with-caption
                            :per-row="2"
                            color="#323232"
                            :images="[images[2].src]"
                            :captions="[images[2].caption]"
                        />
                        <theory-sentences :sentences="sentences.slice(21,23)"/>
                        <theory-sentences is-html :sentences="sentences.slice(23,25)"/>
                        <vue-mathjax :formula="formulas[6]"/>
                        <theory-sentences is-html :sentences="sentences.slice(25,27)"/>
                        <image-with-caption
                            :per-row="2"
                            :start-idx="2"
                            color="#323232"
                            :images="[images[3].src, images[4].src]"
                            :captions="[images[3].caption, images[4].caption]"
                        />
                        <theory-sentences is-html :sentences="sentences.slice(27,28)"/>
                    </v-expansion-panel-content>
                </v-expansion-panel>
            </v-expansion-panels>
            <theory-sentences 
                row-class="mt-1"
                :sentences="sentences.slice(28,32)"
            />
            <vue-mathjax :formula="formulas[7]"/>
            <theory-sentences is-html :sentences="sentences.slice(32,35)"/>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import TheorySentences from '../ui/TheorySentences'
import AudioWithTitle from '../ui/AudioWithTitle.vue'
import ImageWithCaption from '../ui/ImageWithCaption'
import { contents } from '../TheoryContents.js'
export default{
    components: { 
        VueMathjax,
        TheorySentences,
        AudioWithTitle,
        ImageWithCaption
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
        },
        audios() {
            return this.contents.Fourier.audios
        }
    },
}
</script>
