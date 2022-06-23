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
                    <v-col cols="4" sm="4" lg="3">
                        <v-card flat>
                            <v-treeview
                                :items="treeviewItems"
                                dense
                                open-on-click
                                activatable
                                transition
                                @update:active="changeComponent"
                            > 
                                <template #prepend="{ item }">
                                    <v-icon>{{ item.icon }}</v-icon>
                                </template>
                            </v-treeview>
                        </v-card>
                    </v-col>
                    <v-col cols="8" sm="8" lg="9">
                        <component :is="currentComponent" />
                    </v-col>
                </v-row>
            </v-card-text>
        </v-card>
    </v-container>
</template>
<script>
import WhatIsFourier from './Fourier/WhatIsFourier'
import FtFormula from './Fourier/FtFormula'
import WhatIsSpectrogram from './Spectrogram/WhatIsSpectrogram'
import SpectrogramFormula from './Spectrogram/SpectrogramFormula'
import WhatIsImpulse from './IrAnalysis/WhatIsImpulse'
import HowToAnalyze from './IrAnalysis/HowToAnalyze'
import WhatIsAuralisation from './Auralisation/WhatIsAuralisation'
import AuralisationFormula from './Auralisation/AuralisationFormula'
export default{
    components:{
        WhatIsFourier,
        FtFormula,
        WhatIsSpectrogram,
        SpectrogramFormula,
        WhatIsImpulse,
        HowToAnalyze,
        WhatIsAuralisation,
        AuralisationFormula
    },
    data:() => ({
        currentComponent:'what-is-fourier',
        treeviewItems: [
            { 
                name: 'Fourier Transform', 
                children: [
                    { 
                        name: 'What is Fourier Tranform?', 
                        id: 'what-is-fourier',
                        icon: 'mdi-comment-question'
                    },
                    { 
                        name: 'Formula', 
                        id: 'ft-formula',
                        icon: 'mdi-equal'
                    },
                ],
            },
            {
                name: 'Spetrogram',
                children: [
                    { 
                        name: 'What is Spectrogram?',
                        id: 'what-is-spectrogram',
                        icon: 'mdi-comment-question'
                    },
                    { 
                        name: 'Formula',
                        id: 'spectrogram-formula',
                        icon: 'mdi-equal'
                    },
                ]
            },
            { 
                name: 'IR Analysis', 
                children: [
                    { 
                        name: 'What is Impulse Response?', 
                        id: 'what-is-impulse',
                        icon: 'mdi-comment-question'
                    },
                    { 
                        name: 'How to analyse?', 
                        id: 'how-to-analyze',
                        icon: 'mdi-poll'
                    },
                ],
            },
            { 
                name: 'Auralisation', 
                children: [
                    { 
                        name: 'What is Auralisation?', 
                        id: 'what-is-auralisation',
                        icon: 'mdi-comment-question'
                    },
                    { 
                        name: 'Formula', 
                        id: 'auralisation-formula',
                        icon: 'mdi-equal'
                    },
                ],
            },
        ]
        //DrawerItems:[
        //    { title: 'What is Fourier Transform?', icon: 'mdi-chart-bar', to: 'what-is-fourier' },
        //    { title: 'What is Spectrogram?', icon: 'mdi-palette', to: 'what-is-spectrogram'}
        //    //{ title: 'What is Convolution?', icon:'mdi-multiplication', to:'what-is-convolution' },
        //    //{ title: 'Impulse Response', icon:'mdi-chart-ppf', to:'impulse-response' },
        //    //{ title: 'Sound Convolution', icon:'mdi-surround-sound', to:'sound-convolution' },
        //    //{ title: 'IR Analysis', icon:'mdi-sine-wave', to:'ir-analysis' },
        //],

    }),
    methods:{
        changeComponent(idArray){
            if(idArray.length != 0) this.currentComponent = idArray[0];
        }
    }
}
</script>
