<template>
    <v-card color="#323232" flat>
        <v-card-title>Clarity</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences is-html :sentences="sentences.slice(0,2)" />
            <vue-mathjax :formula="formulas[0]"/>
            <theory-sentences is-html :sentences="sentences.slice(2,6)" />
            <v-card flat class="mt-0" color="#323232">
                <v-card-text class="d-flex justify-center pb-0 font-weight-light">
                    Table 3. Clarity in concert halls[4]
                </v-card-text>
                <v-card-text class="pt-0">
                    <v-data-table 
                        class="text-body-2"
                        dense
                        hide-default-footer
                        :headers="clarityHeaders"
                        :items="clarityItems"
                    />
                </v-card-text>
            </v-card>
        </v-card-text>
    </v-card>
</template>
<script>
import TheorySentences from '../../ui/TheorySentences'
import { VueMathjax } from 'vue-mathjax'
export default{
    components:{ 
        TheorySentences,
        VueMathjax 
    },
    data:() => ({
        sentences:[
            'This parameter refers to how clear the sound quality is.',
            '<i>Cn</i> is the energy raito (in decibel) of the first <i>n</i> ms (early sound energy) and the rest of the sequence (later reverberant energy).',
            '<i>C80</i> is a popular objective measure for clarity.',
            "Especially, <i>C80(3)</i>, defined as the average of <i>C80</i> values at 500Hz, 1kHz, and 2kHz octave bands, has been developed to evaluate the room's quality.",
            'Generally, acceptable values for <i>C80(3)</i> for concert halls are between +1dB and -4dB[4].',
            "The following table shows famous concert halls' C80(3) values."
        ],
        formulas:[
            '$$ {\\rm C_{n}} = 10 \\log_{10} ({{\\int_{0}^{n \\times 10^{-3}} p^{2}(t)dt} \\over {\\int_{0.05}^{\\infty} p^{2}(t)dt}}) \\ \\rm{dB} $$',
        ],
        clarityHeaders:[
            { text: 'Concert Hall (unoccupied)', value:'hall'    },
            { text: 'C80(3) (dB)',               value:'clarity' }
        ],
        clarityItems:[
            { hall: 'Amsterdam, Concertgebouw',         clarity: -3.3 },
            { hall: 'Boston, Symphony Hall',            clarity: -2.7 },
            { hall: 'Vienna, Gr. Musikvereinsaal',      clarity: -3.7 },
            { hall: 'Basel, Stadt-Casino',              clarity: -2.3 },
            { hall: 'Berlin, Konzerthaus',              clarity: -2.5 },
            { hall: "Cardiff, Wales, St. David's Hall", clarity: -0.9 },
            { hall: 'Tokyo, Hamarikyu Asahi',           clarity: -0.2},
            { hall: 'Zurich, Großer Tonhallesaal',      clarity: -3.6},
        ]
    }),
}
</script>

