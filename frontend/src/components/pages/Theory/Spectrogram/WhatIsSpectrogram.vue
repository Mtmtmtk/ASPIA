<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Spectrogram?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences
                row-class="mt-0" 
                :sentences="sentences.slice(0,4)"
            />
            <image-with-caption
                :images="images.map(el => el.src).slice(0,1)"
                :captions="images.map(el => el.caption).slice(0,1)"
            />
            <theory-sentences
                :sentences="sentences.slice(4,5)"
            />
            <theory-sentences
                :sentences="sentences.slice(5,7)"
            />
            <vue-mathjax :formula="formulas[0]"/>
            <theory-sentences
                is-html
                :sentences="sentences.slice(7,8)"
            />
            <audio-with-title
                :title="audios[0].title"
                :src="audios[0].src"
            />
            <theory-sentences
                row-class="mt-2"
                :sentences="sentences.slice(8,11)"
            />
            <image-with-caption
                :start-idx="2"
                :images="images.map(el => el.src).slice(1,2)"
                :captions="images.map(el => el.caption).slice(1,2)"
            />
            <theory-sentences
                row-class="mt-2"
                :sentences="sentences.slice(11,13)"
            />
            <theory-sentences
                :sentences="sentences.slice(13,17)"
            />
            <theory-sentences
                :sentences="sentences.slice(17,20)"
            />
            <image-with-caption
                :start-idx="3"
                :images="images.map(el => el.src).slice(2,4)"
                :captions="images.map(el => el.caption).slice(2,4)"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import AudioWithTitle from '../ui/AudioWithTitle.vue'
import { contents } from '../TheoryContents.js'
export default {
    components: {
        VueMathjax,
        ImageWithCaption,  
        TheorySentences,
        AudioWithTitle
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
        },
        audios() {
            return this.contents.Spectrogram.audios
        }
    },
}
</script>
