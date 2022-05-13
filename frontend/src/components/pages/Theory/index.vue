<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Theory</font>
            </v-col>
        </v-row>
        <v-card 
            flat
            dark
            color="#323232"
            class="mt-5"
        >
            <v-card-text>
                <v-row>
                    <v-col cols="3">
                        <v-card flat>
                            <v-list>
                                <v-list-item 
                                    v-for="item in drawerItems"
                                    :key="item.val"
                                    @click="changeComponent(item.to)"
                                >
                                    <v-list-item-icon>
                                        <v-icon>{{ item.icon }}</v-icon>
                                    </v-list-item-icon>
                                    <v-list-item-content>
                                        <v-list-item-title>{{ item.title }}</v-list-item-title>
                                    </v-list-item-content>
                                </v-list-item>
                            </v-list>
                        </v-card>
                    </v-col>
                    <v-col cols="9">
                        <component :is="currentComponent" />
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-container>
</template>
<script>
import WhatIsConvolution from './WhatIsConvolution'
import ImpulseResponse from './ImpulseResponse'
import SoundConvolution from './SoundConvolution'
import IrAnalysis from './IrAnalysis'
export default{
    components:{
        WhatIsConvolution,
        ImpulseResponse,
        SoundConvolution,
        IrAnalysis
    },
    data:() => ({
        currentComponent:'what-is-convolution',
        drawerItems:[
            { title: 'What is convolution?', icon:'mdi-multiplication', to:'what-is-convolution' },
            { title: 'Impulse response', icon:'mdi-chart-ppf', to:'impulse-response' },
            { title: 'Sound convolution', icon:'mdi-surround-sound', to:'sound-convolution' },
            { title: 'IR Analysis', icon:'mdi-sine-wave', to:'ir-analysis' },
        ]
    }),
    methods:{
        changeComponent(url){
            this.currentComponent = url;
        }
    }
}
</script>
