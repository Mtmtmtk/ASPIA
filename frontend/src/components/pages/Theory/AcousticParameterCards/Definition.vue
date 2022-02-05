<template>
    <v-card color='#323232' flat>
        <v-card-title>Definition</v-card-title>
        <v-card-text class='text-body-1'>
            <v-row><v-col>{{sentences[0] + ' ' + sentences[1]}}</v-col></v-row>   
            <vue-mathjax :formula='formulas[0]'/>
            <v-row><v-col>{{sentences[2] + ' ' + sentences[3]}}</v-col></v-row>   
            <v-row class='pt-0 mt-0 text-center'><v-col>Table 4. Definition and its score[6]</v-col></v-row>
            <v-data-table 
                class='text-body-2'
                dense
                hide-default-footer
                :headers='definitionHeaders'
                :items='definitionItems'
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
            'The parameter Dn is one of the parameters that explain a speech intelligibility.',
            'Dn can be calculated by the energy ratio (in decibel) of the first n ms and the entire sequence.',
            'D50 is a popular objective measure for definition.',
            'Marshall[6] suggested this value and defined the evaluation of the speech intelligibility as follows:'
        ],
        formulas:[
            '$$ {\\rm D_{n}} = {{\\int_{0}^{n \\times 10^{-3}} p^{2}(t)dt} \\over {\\int_{0}^{\\infty} p^{2}(t)dt}} $$'
        ],
        definitionHeaders:[
            { text: 'Score', value: 'score' },
            { text: 'D50 (%)', value: 'definition' }
        ],
        definitionItems:[
            { score: 'Excellent', definition: '0.86 - 1.00' },
            { score: 'Good', definition: '0.67 - 0.86' },
            { score: 'Fair', definition: '0.39 - 0.67' },
            { score: 'Poor', definition: '0.17 - 0.39' },
            { score: 'Bad', definition: '0.06 - 0.17' },
        ],
    }),
}
</script>

