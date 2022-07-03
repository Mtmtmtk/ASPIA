<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>Formula</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences
                row-class="mt-0" 
                :sentences="sentences.slice(20,22)"
            />
            <v-row class="d-flex justify-center">
                <v-col cols="4" class="py-0">
                    <v-card flat tile><v-img :src="images[4].src"/></v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col class="pt-0">
                    <span class="d-flex justify-center font-weight-thin" style="color: #BDBDBD; font-size: 14px;"> Fig. 1. {{ images[4].caption }}</span>
                </v-col>
            </v-row>
            <theory-sentences
                row-class="mt-0" 
                :sentences="sentences.slice(22,25)"
            />
            <vue-mathjax :formula="formulas[1]" />
            <image-with-caption
                :start-idx="2"
                :per-row="2"
                :images="[ images[5].src ]"
                :captions="[ images[5].caption ]"
            />
            <theory-sentences
                row-class="mt-0" 
                is-html
                :sentences="sentences.slice(25,27)"
            />
            <vue-mathjax :formula="formulas[2]" />
            <theory-sentences
                row-class="mt-0" 
                is-html
                :sentences="sentences.slice(27,31)"
            />
            <image-with-caption
                :start-idx="3"
                :per-row="1"
                image-width="400"
                :images="[ images[6].src ]"
                :captions="[ images[6].caption ]"
            />
        </v-card-text>  
    </v-card>
</template>
<script>
import ImageWithCaption from '../ui/ImageWithCaption'
import { VueMathjax } from 'vue-mathjax'
import TheorySentences from '../ui/TheorySentences'
import { contents } from '../TheoryContents.js'
export default {
    components: {
        ImageWithCaption,  
        VueMathjax,
        TheorySentences
    },
    data: () => ({
        contents
    }),
    computed:{
        sentences() {
            return this.contents.Spectrogram.sentences
        },
        formulas() {
            return this.contents.Spectrogram.formulas
        },
        images() {
            return this.contents.Spectrogram.images
        }
    },
}
</script>
