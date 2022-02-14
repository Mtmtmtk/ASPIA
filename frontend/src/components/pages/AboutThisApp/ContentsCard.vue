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
                'This app is an integrated sound processing tool.',
                'You can analyse an impulse response, convolute an anechoice sound with an impulse response, and study their theories.',
                'Do you think they are challenging?',
                'The answer is "No"!',
                'This app is accessible for anybody who does not have an academic signal processing background, so you can do it by following the instructions!'
            ],
            [
                'This app has four sections: Convolution generator, Impulse response analysis, Theory, and Resources.',
            ],
            [
                'Convolution generator (Generator in the sidebar) guides creating a convoluted sound from your recording or an anechoic sound you register.',
                'There are seven steps to follow, and you can make your recording as if it is recorded in a concert hall, a church, and even a place already collapsed!',
                'The impulse response data are provided by Openair, which was developed by Audiolab, Department of Electronics, University of York.',
                'Please click the upper-left banner and go to the offcial website of Openair to see its further information.'
            ],
            [
                'The impulse response analysis (IR Analysis) section enables you to analyse an IR without any academic knowledge of signal processing!',
                'All you have to do is inputting an IR, and you will get a lot of acoustic parameters and other elements that characterise the IR.',
                'If you are confident with such an academic field, you can customise filters and see the result to compare the effect of the filter!',
                'It is not only easy but also flexible!'
            ],
            [
                'For those who want to understand what is happening in the background, the Theory section provides everything you should learn.',
                'This section requires at least high-school mathematics knowledge, yet it is straightforward to master the signal processing skills only by following this section.',
                'Please take time to read it if you are willing to learn it!'
            ],
            [
                'The last section is Resources, a warehouse of the information of the spaces used in the Generator section.',
                "This section shows each spaces' exterior, interior, sample impulse response, and fundamental acoustic parameters.",
                'Please use this section to feel what space sounds like and apply it to the convolution.'
            ],
            [
                'If you have any problems or find errors, please email Motoki Saito (developer of this app!) at ms2676@york.ac.uk.',
            ]
        ]
    })
}
</script>
