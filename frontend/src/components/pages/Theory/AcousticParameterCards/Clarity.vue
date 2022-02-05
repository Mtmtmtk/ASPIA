<template>
    <v-card color='#323232' flat>
        <v-card-title>Clarity</v-card-title>
        <v-card-text class='text-body-1'>
            <v-row><v-col>{{sentences[0] + ' ' + sentences[1]}}</v-col></v-row>   
            <vue-mathjax :formula='formulas[0]'/>
            <v-row><v-col>{{sentences[2] + ' ' + sentences[3] + ' ' + sentences[4] + ' ' + sentences[5]}}</v-col></v-row>   
            <v-row class='pt-0 mt-0 text-center'><v-col>Table 3. Clarity in concert halls[5]</v-col></v-row>
            <v-data-table 
                class='text-body-2'
                dense
                hide-default-footer
                :headers='clarityHeaders'
                :items='clarityItems'
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
export default{
    components:{ VueMathjax },
    data:() => ({
        sentences:[
            'The parameter C refers to how clear the sound quality is.',
            'Cn is the energy raito (in decibel) of the first n ms (early sound enegy) and the rest of the sequence (later reverberant energy).',
            'C80 is a popular objective measure for clarity.',
            "Espeacially, C80(3), which is defined as the average of C80 values at 500Hz, 1kHz, and 2kHz octave bands, has been developed to evaluate what a room's quality is.",
            'In general, acceptable values for C80(3) for concert halls are between +1dB and -4dB.[5]',
            'The follwing table is the C80(3) values of famous concert halls.'
        ],
        formulas:[
            '$$ {\\rm C_{n}} = 10 \\log_{10} ({{\\int_{0}^{n \\times 10^{-3}} p^{2}(t)dt} \\over {\\int_{0.05}^{\\infty} p^{2}(t)dt}}) \\ \\rm{dB} $$',
        ],
        clarityHeaders:[
            { text: 'Concert Hall (unoccupied)', value:'hall' },
            { text: 'C80(3) (dB)', value:'clarity' }
        ],
        clarityItems:[
            { hall:'Amsterdam, Concertgebouw', clarity: -3.3 },
            { hall:'Boston, Symphony Hall', clarity: -2.7 },
            { hall:'Vienna, Gr. Musikvereinsaal', clarity: -3.7 },
            { hall:'Basel, Stadt-Casino', clarity: -2.3 },
            { hall:'Berlin, Konzerthaus', clarity: -2.5 },
            { hall:"Cardiff, Wales, St. David's Hall", clarity: -0.9 },
            { hall:'Tokyo, Hamarikyu Asahi', clarity: -0.2},
            { hall:'Zurich, Großer Tonhallesaal', clarity: -3.6},
        ]
    }),
}
</script>

