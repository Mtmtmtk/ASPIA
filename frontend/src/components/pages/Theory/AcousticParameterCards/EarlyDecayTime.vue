<template>
    <v-card color="#323232" flat>
        <v-card-title>Early Decay Time</v-card-title>
        <v-card-text class="text-body-1">
            <v-row><v-col>{{sentences[0] + ' ' + sentences[1]}}</v-col></v-row>   
            <vue-mathjax :formula="formulas[0]"/>
            <v-row><v-col>{{sentences[2]}}</v-col></v-row>
            <v-row class="pt-0 mt-0 text-center"><v-col>Table 2. Early Decay Time in concert halls[4]</v-col></v-row>
            <v-data-table 
                class="text-body-2"
                dense
                hide-default-footer
                :items-per-page="20"
                :headers="EDTHeaders"
                :items="EDTItems"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
export default{
    components:{
        VueMathjax
    },
    data:() => ({
        EDTHeaders:[
            { text: 'Hall', value:'hall'},
            { text: '125Hz', value:'125'},
            { text: '250Hz', value:'250'},
            { text: '500Hz', value:'500'},
            { text: '1kHz', value:'1k'},
            { text: '2kHz', value:'2k'}
        ],
        EDTItems:[
            { hall:'Royal Festival Hall, London',               125:1.33, 250:1.37, 500:1.43, "1k":1.57, "2k":1.66},
            { hall:'Royal Albert Hall, London',                 125:2.53, 250:2.54, 500:2.67, "1k":2.63, "2k":2.62},
            { hall:'Queen Elizabeth Hall, London',              125:1.70, 250:1.67, 500:2.04, "1k":2.12, "2k":2.24},
            { hall:'Barbican Concert Hall, London',             125:1.92, 250:1.82, 500:1.84, "1k":1.96, "2k":2.04},
            { hall:'Wigmore Hall, London',                      125:1.49, 250:1.61, 500:1.55, "1k":1.57, "2k":1.48},
            { hall:'Fairfield Hall, Croydon',                   125:2.18, 250:1.98, 500:1.89, "1k":1.85, "2k":1.73},
            { hall:'Wessex Hall, Poole',                        125:2.48, 250:1.77, 500:1.66, "1k":1.63, "2k":1.51},
            { hall:'Colston Hall, Bristol',                     125:2.08, 250:1.96, 500:1.81, "1k":1.87, "2k":1.78},
            { hall:"St. David's, Cardiff",                      125:1.90, 250:2.13, 500:2.11, "1k":2.14, "2k":2.11},
            { hall:'Assembly Hall, Watford',                    125:1.53, 250:1.74, 500:1.58, "1k":1.47, "2k":1.25},
            { hall:'Music School Auditorium, Cambridge',        125:1.99, 250:1.94, 500:2.08, "1k":2.11, "2k":2.00},
            { hall:'Royal Concert Hall, Nottigham',             125:2.77, 250:2.10, 500:1.72, "1k":1.77, "2k":1.57},
            { hall:'Free Trade Hall, Manchester',               125:1.47, 250:1.47, 500:1.65, "1k":1.77, "2k":1.62},
            { hall:'Philharmonic Hall, Liverpool',              125:1.89, 250:1.78, 500:1.80, "1k":1.78, "2k":1.59},
            { hall:'Usher Hall, Edinburgh',                     125:2.01, 250:1.97, 500:2.08, "1k":2.22, "2k":2.12},
            { hall:'Conference Centre, Wembley',                125:1.73, 250:1.61, 500:1.17, "1k":1.12, "2k":0.91},
            { hall:'Butterworth Hall, Warwick University',      125:2.28, 250:2.77, 500:2.69, "1k":2.32, "2k":1.89},
            { hall:'Christchurch Town Hall, New Zealand',       125:1.97, 250:1.77, 500:2.03, "1k":2.14, "2k":2.11},
            { hall:'Michael Fowler Centre, Wellington, NZ',     125:1.69, 250:1.82, 500:1.86, "1k":1.81, "2k":1.82},
            { hall:'Segerstrom Hall, Orange County, California',125:2.36, 250:2.44, 500:2.30, "1k":2.38, "2k":2.20},
        ],
        sentences:[
            'Early Decay Time describes a subjective feeling of reverberation rather than RT60.',
            "This parameter can be calculated as a time that the Schroeder Curve's extrapolation of 0 dB and -10 dB crosses -60 dB point.",
            'Barron[4] measured and calculated the EDT in many British concert halls and revealed that most of them are between 1.5 and 2.5 seconds.'
        ],
        formulas:[
            '$$ {\\rm EDT} = 6 T_{-10} \\ \\rm{sec.}$$',
        ],
    }),
}
</script>
