<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Fourier Transform?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences :sentences="sentences.slice(0,2)"/>
            <image-with-caption
                :per-row="2"
                :images="images.map(el => el.src)"
                :captions="images.map(el => el.caption)"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import { contents } from '../TheoryContents.js'
export default{
    components: { 
        ImageWithCaption,
        TheorySentences
    },
    data:() => ({
        contents,
    }),
    computed:{
        sentences() {
            return this.contents.Fourier.sentences
        },
        images() {
            return this.contents.Fourier.images
        }
    },
}
</script>
