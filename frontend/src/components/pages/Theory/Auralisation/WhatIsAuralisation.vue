<template>
    <v-card flat class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Auralisation?</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences :sentences="sentences.slice(0,2)"/>
            <audio-with-title
                :title="audios[0].title"
                :src="audios[0].src"
            />
            <br>
            <theory-sentences :sentences="sentences.slice(2,3)"/>
            <audio-with-title
                :title="audios[1].title"
                :src="audios[1].src"
            />
            <br>
            <theory-sentences :sentences="sentences.slice(3,4)"/>
            <audio-with-title
                :title="audios[2].title"
                :src="audios[2].src"
            />
            <br>
            <theory-sentences :sentences="sentences.slice(4,6)"/>
        </v-card-text>
    </v-card>
</template>
<script>
//import ImageWithCaption from '../ui/ImageWithCaption'
import TheorySentences from '../ui/TheorySentences'
import AudioWithTitle from '../ui/AudioWithTitle.vue'
//import VAudio from '@/components/ui/VAudio'
import { contents } from '../TheoryContents.js'
export default{
    components: { 
        //ImageWithCaption,
        TheorySentences,
        AudioWithTitle
        //VAudio
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
        audios() {
            return this.contents.Auralisation.audios
        }
    }, 
}
</script>
