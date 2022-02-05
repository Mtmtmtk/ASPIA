<template>
    <v-card color='#323232' flat>
        <v-card-title>Reverberation Time (RT60)</v-card-title>
        <v-card-text class='text-body-1'>
            <v-row><v-col>{{sentences[0] + ' ' + sentences[1]}}</v-col></v-row>   
            <vue-mathjax :formula='formulas[0]' />
            <v-row><v-col>{{sentences[2] + ' ' + sentences[3]}}</v-col></v-row>   
            <v-img 
                class='mt-1'
                max-height='300'
                contain
                :src='images[0]'
            />
            <v-row class='pt-0 mt-0 text-center'><v-col>Fig.2. Optimum RT60 in the middle frequency range [2]</v-col></v-row>
            <v-row class='pt-0 mt-0 text-center'><v-col>Table 2. Reverberation Time in concert halls[3]</v-col></v-row>
            <v-data-table 
                class='text-body-2'
                dense
                hide-default-footer
                :headers='RTHeaders'
                :items='RTItems'
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
export default{
    data:() => ({
        coomponents:{ VueMathjax },
        sentences:[
            'Reverberation time is a measure of the time required for reflecting sound to "fade away" in an enclosed area after the source of the sound has stopped.',
            'This parameter can be calculated as a time that the extrapolation of -5 dB and -35 dB crosses -60 dB point.',
            "The ideal RT60 depends on the space's purpose and volume.",
            "Doelle defined the appropriate RT60 for the studios in the 500-1000 Hz range. (See Fig.2.)",
        ],
        formulas:[
            '$$ {\\rm RT_{60}} = {11 \\over 6} T_{-35} - {5 \\over 6} T_{-5} \\ \\rm{sec.} $$',
        ],
        images:[
            require('@/assets/theory/rt60.jpg')
        ],
        RTHeaders:[
            { text: 'Concert Hall', value:'hall' },
            { text: 'RT at 500Hz occupied', value:'occupied' },
            { text: 'RT at 500Hz unoccupied', value:'unoccupied' }
        ],
        RTItems:[
            { hall:'Amsterdam, Concertgebouw',         occupied: 2.05, unoccupied:2.55},
            { hall:'Boston, Symphony Hall',            occupied: 1.85, unoccupied:2.40},
            { hall:'Vienna, Gr. Musikvereinsaal',      occupied: 2.04, unoccupied:3.06},
            { hall:'Basel, Stadt-Casino',              occupied: 1.80, unoccupied:2.31},
            { hall:'Berlin, Konzerthaus',              occupied: 2.00, unoccupied:2.51},
            { hall:"Cardiff, Wales, St. David's Hall", occupied: 1.96, unoccupied:2.09},
            { hall:"New York, Carnegie Hall",          occupied: 1.80, unoccupied:2.10},
            { hall:'Tokyo, Hamarikyu Asahi',           occupied: 1.65, unoccupied:1.83},
            { hall:'Zurich, Großer Tonhallesaal',      occupied: 2.15, unoccupied:3.27},
        ]
    }),
}
</script>
