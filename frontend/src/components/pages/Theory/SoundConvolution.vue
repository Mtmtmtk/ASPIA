<template>
    <v-card height="570" class="ma-0 pa-0 overflow-auto">
        <v-card-title>Sound Convolution</v-card-title>
        
        <v-card-text class="text-h5 py-0 my-0">
            Convolution steps in this app
        </v-card-text>
        <v-card-text class="text-body-1 pt-3 mt-2">
            <v-row v-for="step,i in steps" :key="step">
                <v-col>
                    {{ `Step${i}: ` + step}}
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
//import { VueMathjax } from 'vue-mathjax'
export default{
    //components:{ VueMathjax },
    data:() => ({
        steps:[
            'Normalise an input sound file and convert the amplitudes that is smaller than 0.0001 into 0.',
            'Resample IR file to the same sampling frequncy as the input sound file, and change IR format into that an user selected.'
        ],
        formulas:[
        ],
    }),
}
</script>
