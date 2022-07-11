<template>
    <v-card color="#323232" flat>
        <v-card-title>Reverberation Time (RT60)</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences is-html :sentences="sentences.slice(0,5)" />
            <vue-mathjax :formula="formulas[0]" />
            <theory-sentences is-html :sentences="sentences.slice(5,6)" />
            <image-with-caption
                color="#323232"
                :start-idx="2"
                :images="images.map(el => el.src).slice(0,1)"
                :captions="images.map(el => el.caption).slice(0,1)"
            />    
            <v-card flat class="mt-0" color="#323232">
                <v-card-text class="d-flex justify-center pb-0 font-weight-light">
                    Table 2. Reverberation Time in concert halls[3]
                </v-card-text>
                <v-card-text class="pt-0">
                    <v-data-table 
                        class="text-body-2"
                        dense
                        hide-default-footer
                        :headers="RTHeaders"
                        :items="RTItems"
                    />
                </v-card-text>
            </v-card>
        </v-card-text>
    </v-card>
</template>
<script>
import ImageWithCaption from '../../ui/ImageWithCaption'
import TheorySentences from '../../ui/TheorySentences'
import { VueMathjax } from 'vue-mathjax'
export default{
    components: { 
        ImageWithCaption,
        TheorySentences,
        VueMathjax 
    },
    data:() => ({
        sentences:[
            'Reverberation time is a measure of the time required for reflecting sound to "fade away" in an enclosed area after the source of the sound has stopped.',
            'This parameter can be calculated as the time at the Schroeder Curve decreasing to -60 dB.',
            'However, it is sometimes difficult to get the parameter from the definition depending on the quality of the receiver, as the low quality receiver cannot accurately record the response down to -60 dB.',
            'In that case, <i>RT60</i> can be calculated alternatively as the time at the linear regression (two points of -5 and -35 dB) of the Schroeder Curve decreasing to -60 dB.',
            'This app applies this alternative method to calculate the reverberation time.',
            "Doelle[2] defined the appropriate <i>RT60</i> for the studios in the 500-1000 Hz range. (See Fig.2.)",
        ],
        formulas:[
            '$$ {\\rm RT_{60}} = {11 \\over 6} T_{-35} - {5 \\over 6} T_{-5} \\ \\rm{sec.} $$',
        ],
        images:[
            { src: require('@/assets/theory/rt60.jpg'), caption: 'Optimum RT60 in the middle frequency range [1]' }
        ],
        RTHeaders:[
            { text: 'Concert Hall',           value: 'hall'       },
            { text: 'RT at 500Hz occupied',   value: 'occupied'   },
            { text: 'RT at 500Hz unoccupied', value: 'unoccupied' }
        ],
        RTItems:[
            { hall: 'Amsterdam, Concertgebouw',         occupied: 2.05, unoccupied: 2.55 },
            { hall: 'Boston, Symphony Hall',            occupied: 1.85, unoccupied: 2.40 },
            { hall: 'Vienna, Gr. Musikvereinsaal',      occupied: 2.04, unoccupied: 3.06 },
            { hall: 'Basel, Stadt-Casino',              occupied: 1.80, unoccupied: 2.31 },
            { hall: 'Berlin, Konzerthaus',              occupied: 2.00, unoccupied: 2.51 },
            { hall: "Cardiff, Wales, St. David's Hall", occupied: 1.96, unoccupied: 2.09 },
            { hall: "New York, Carnegie Hall",          occupied: 1.80, unoccupied: 2.10 },
            { hall: 'Tokyo, Hamarikyu Asahi',           occupied: 1.65, unoccupied: 1.83 },
            { hall: 'Zurich, Großer Tonhallesaal',      occupied: 2.15, unoccupied: 3.27 },
        ]
    }),
}
</script>
