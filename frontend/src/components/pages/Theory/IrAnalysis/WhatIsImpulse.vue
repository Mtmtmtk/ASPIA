<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Impulse Response?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences
                is-html
                :sentences="sentences.slice(0,1)"
            />
            <vue-mathjax :formula="formulas[0]" />
            <theory-sentences
                is-html
                :sentences="sentences.slice(1,2)"
            />
            <vue-mathjax :formula="formulas[1]" />
            <theory-sentences
                is-html
                :sentences="sentences.slice(2,5)"
            />
            <theory-sentences
                is-html
                :sentences="sentences.slice(5,9)"
            />
            <image-with-caption
                :per-row="3"
                :images="images.map(el => el.src).slice(0,3)"
                :captions="images.map(el => el.caption).slice(0,3)"
            />
            <theory-sentences
                row-class="mt-0"
                is-html
                :sentences="sentences.slice(9,11)"
            />
            <theory-sentences
                row-class="mt-0"
                is-html
                :sentences="sentences.slice(11,12)"
            />
            <vue-mathjax :formula="formulas[2]" />
            <image-with-caption
                :start-idx="4"
                :per-row="1"
                :images="images.map(el => el.src).slice(3,4)"
                :captions="images.map(el => el.caption).slice(3,4)"
            />
            <theory-sentences
                row-class="mt-0"
                is-html
                :sentences="sentences.slice(12,14)"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import { VueMathjax } from 'vue-mathjax'
import { contents } from '../TheoryContents.js'
export default {
    components: {
        ImageWithCaption,  
        TheorySentences,
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
