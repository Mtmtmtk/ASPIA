<template>
    <v-card flat height='570' class='ma-0 pa-0 overflow-auto'>
        <v-card-title>What is Convolution?</v-card-title>
        <v-card-text class='text-body-1'>
            <v-row><v-col>{{sentences[0]}}</v-col></v-row>
            <vue-mathjax :formula='formulas[0]'/>
            <v-row><v-col>{{sentences[1]}}</v-col></v-row>
            <v-img 
                class='my-1'
                max-height='150'
                contain
                :src='convolutionGif'
            />
            <v-row><v-col>{{sentences[2]}}</v-col></v-row>
            <vue-mathjax :formula='formulas[1]'/>
            <v-row><v-col>{{sentences[3] + ' ' + sentences[4]}}</v-col></v-row>
            <vue-mathjax :formula='formulas[2]'/>
            <vue-mathjax :formula='formulas[3]'/>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import { contents } from './TheoryContents.js'
export default{
    components:{ VueMathjax },
    data:() => ({
        contents:contents,
    }),
    computed:{
        sentences(){
            return this.contents.WhatIsConvolution.sentences
        },
        formulas(){
            return this.contents.WhatIsConvolution.formulas
        },
        convolutionGif(){
            return this.contents.WhatIsConvolution.images[0]
        }
    },
}
</script>
