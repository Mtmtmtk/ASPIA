<template>
    <v-card color="#323232" flat>
        <v-card-title>Definition</v-card-title>
        <v-card-text class="text-body-1">
            <theory-sentences is-html :sentences="sentences.slice(0,2)" />
            <vue-mathjax :formula="formulas[0]"/>
            <theory-sentences is-html :sentences="sentences.slice(2,4)" />
            <v-card flat class="mt-0" color="#323232">
                <v-card-text class="d-flex justify-center pb-0 font-weight-light">
                    Table 4. Definition and its score[5]
                </v-card-text>
                <v-card-text class="pt-0">
                    <v-data-table 
                        class="text-body-2"
                        dense
                        hide-default-footer
                        :headers="definitionHeaders"
                        :items="definitionItems"
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
            'The parameter <i>Dn</i> is one of the parameters that explain speech intelligibility.',
            '<i>Dn</i> can be calculated by the energy ratio (in percentage) of the first <i>n</i> ms and the entire sequence.',
            '<i>D50</i> is a popular objective measure for definition.',
            'Marshall[5] suggested this value and defined the evaluation of the speech intelligibility as follows:'
        ],
        formulas:[
            '$$ {\\rm D_{n}} = {{\\int_{0}^{n \\times 10^{-3}} p^{2}(t)dt} \\over {\\int_{0}^{\\infty} p^{2}(t)dt}} $$'
        ],
        definitionHeaders:[
            { text: 'Score',   value: 'score' },
            { text: 'D50 (%)', value: 'definition' }
        ],
        definitionItems:[
            { score: 'Excellent', definition: '0.86 - 1.00' },
            { score: 'Good',      definition: '0.67 - 0.86' },
            { score: 'Fair',      definition: '0.39 - 0.67' },
            { score: 'Poor',      definition: '0.17 - 0.39' },
            { score: 'Bad',       definition: '0.06 - 0.17' },
        ],
    }),
}
</script>

