<template>
    <v-card flat height="570" class="ma-0 pa-0 overflow-auto">
        <v-card-title>Impulse Response</v-card-title>
        <v-card-text class="text-body-1">
            <v-row><v-col>{{sentences[0] + " " + sentences[1]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[0]"/>
            <v-row><v-col>{{sentences[2]}}</v-col></v-row>
            <v-img 
                class="my-1"
                max-height="150"
                contain
                :src="IRGif"
            />
            <v-row><v-col>{{sentences[3]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[1]"/>
            <v-row><v-col>{{sentences[4] + " " + sentences[5]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[2]"/>
            <v-row><v-col>{{sentences[6]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[3]"/>
            <v-row><v-col>{{sentences[7]}}</v-col></v-row>
            <vue-mathjax :formula="formulas[4]"/>
            <v-row><v-col>{{sentences[8]}}</v-col></v-row>
            <v-row><v-col>{{sentences[9] + " " + sentences[10]}}</v-col></v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
import { contents } from './TheoryContents.js'
export default{
    components:{ VueMathjax },
    data:() => ({
        contents:contents
    }),
    computed:{
        sentences(){
            return this.contents.ImpulseResponse.sentences
        },
        formulas(){
            return this.contents.ImpulseResponse.formulas
        },
        IRGif(){
            return this.contents.ImpulseResponse.images[0]
        }
    }
}
</script>
