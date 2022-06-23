<template>
    <v-card dark color="#323232">
        <v-card-title>Hello!</v-card-title>
        <v-card-text class="text-body-1">
            <v-row 
                v-for="paragraph,i in paragraphs" 
                :key="`paragraph_no_${i}`"
            >
                <v-col>
                    <span
                        v-for="text,j in paragraph"
                        :key="`text_no_${j}`"
                    >{{text}}
                    </span>
                </v-col>
            </v-row>
            <v-row class="text-h6">
                <v-col class="pb-0">
                    Developed and maintained by:
                </v-col>
            </v-row>
            <v-row class="text-body-1">
                <v-col class="pt-0">
                Motoki Saito, Audio and Music Technology MSc, Department of Electronic Engineering, University of York
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
export default{
    data:()=>({
        paragraphs:[
            [
                'ASPIA (IPA: /eɪspiə/) is the multi-functional acoustic signal processing (ASP) app using the OpenAIR database.',
                'This application is developed as part of my MSc plan, which aims to create a new interactive ASP app that expands the functionality of the OpenAIR database and makes the ASP more accessible for everyone.',
                "The main feature of this app is the compatibility of simplicity and flexibility; there are many settings of the signal processing that the user can change, whereas the app doesn't require any knowledge from the user for the basic process.",
            ],
            [
                'This app has five sections; Auralisation, Impulse response (IR) analysis, Spectrogram, Theory, and Resources.'
            ],
            [
                'The Auralisation section enables you to create the auralised sound.',
                'Auralisation is the technique of making an acoustic virtual reality; it is possible to reproduce a reverberant sound as if the sound source is played in an arbitrary space.',
                'Usually, it is necessary to code the programming language to implement it; however, using this app, what you have to do is only to follow the instructions!',
                'The prepared data of spaces are collected from the OpenAIR database.'
            ],
            [
                'IR Analysis section lets you explore the acoustic characteristics of the spaces.',
                'Once you submit an impulse response and click the "Start Analysis" button, the system immediately calculates the Schroeder curve and acoustic parameters!',
                "If you are confident with acoustic signal processing, you can customise filters and see the result to compare the filter's effect.",
            ],
            [
                'The Spectrogram section helps you to create the spectrograms, which is tiresome to code.',
                'The procedure is the same as IR analysis - just input the sound file and press the "Create Spectrogram" button.',
                'You can also change the settings such as the window function, overlapping percentage, and sampling points.'
            ],
            [
                'If you want to know what is happening in the background system, please look at the Theory section.',
                'In the section, the description of the mathematical theories and acoustic parameters are written from the beginning.'
            ],
            [
                'The Resources section introduces the information about the spaces/rooms whose impulse responses are prepared in the Auralisation section.',
                "That information includes the exterior, interior, sample impulse response, and acoustic parameters at the representative position."
            ],
            [
                'If you have any problems or find errors, please email Motoki Saito (developer of this app!) at ms2676@york.ac.uk.',
            ]
        ]
    })
}
</script>
