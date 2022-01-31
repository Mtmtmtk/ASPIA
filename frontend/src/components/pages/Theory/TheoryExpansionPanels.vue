<template>
    <v-expansion-panels
        dark
        focusable
        hover
    >
        <v-expansion-panel>
            <v-expansion-panel-header>
                Sound Convolution
            </v-expansion-panel-header>
            <v-expansion-panel-content>
                <v-card 
                    height='600' 
                    color='#323232' 
                    class='mt-5'
                >
                    <v-card-text>
                        <v-row>
                            <v-col cols='3'>
                                <v-card>
                                    <v-list>
                                        <v-list-item 
                                            v-for='item in drawerItems'
                                            :key='item.val'
                                            @click='changeComponent(item.to)'
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
                            <v-col cols='9'>
                                <component :is='currentComponent'/>
                            </v-col>
                        </v-row>
                    </v-card-text>
                </v-card>
            </v-expansion-panel-content>
        </v-expansion-panel>
        <v-expansion-panel>
            <v-expansion-panel-header>
                IR Analysis
            </v-expansion-panel-header>
            <v-expansion-panel-content>
                aaaaa
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>
<script>
import WhatIsConvolution from './WhatIsConvolution'
import ImpulseResponse from './ImpulseResponse'
import SoundConvolution from './SoundConvolution'
export default{
    components:{
        WhatIsConvolution,
        ImpulseResponse,
        SoundConvolution
    },
    data:() => ({
        currentComponent:'what-is-convolution',
        drawerItems:[
            { title: 'What is convolution?', icon:'mdi-multiplication', to:'what-is-convolution' },
            { title: 'Impulse response', icon:'mdi-chart-ppf', to:'impulse-response' },
            { title: 'Sound convolution', icon:'mdi-surround-sound', to:'sound-convolution' },
        ]
    }),
    methods:{
        changeComponent(url){
            this.currentComponent = url;
            console.log(this.currentComponent)
        }
    }
}
</script>
