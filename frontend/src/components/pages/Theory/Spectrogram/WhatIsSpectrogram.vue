<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Spectrogram?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences
                row-class="mt-0" 
                :sentences="sentences[0]"
            />
            <theory-sentences
                :sentences="sentences.slice(1,4)"
            />
            <theory-sentences
                :sentences="sentences.slice(4,7)"
            />
            <image-with-caption
                :images="images.map(el => el.src).slice(0,2)"
                :captions="images.map(el => el.caption).slice(0,2)"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import { contents } from '../TheoryContents.js'
export default {
    components: {
        ImageWithCaption,  
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
