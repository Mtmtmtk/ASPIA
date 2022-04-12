<template>
    <v-data-table
        :headers="headers"
        :items="items"
        :class="colorClass"
        hide-default-footer
    >
        <template v-slot:item.parameter="{ item }">
            <v-tooltip 
                bottom 
                color="#004D40"
                max-width="400"
            >
                <template v-slot:activator="{ on }">
                    <span v-on="on">{{ item.parameter }}</span>
                </template>
                <p class="text-h6 pb-0 mb-0">{{item.parameter}}</p>
                <p class="text-b1 pt-0 mt-0 text-justify">{{tooltipText[item.parameter]}}</p>
                <vue-mathjax :formula="formula[item.parameter]" />
            </v-tooltip>
        </template>
    </v-data-table>
</template>
<script>
import { octaveBands } from '../pages/library.js'
import { VueMathjax } from 'vue-mathjax'
export default{
    components:{ VueMathjax },
    data: () => ({
        octaveBands,
        formula:{
            'RT60 (s)': '$$ {\\rm RT_{60}} = {11 \\over 6} T_{-35} - {5 \\over 6} T_{-5} $$',
            'EDT (s)':'$$ {\\rm EDT} = 6 T_{-10} $$',
            'D50':'$$ {\\rm D_{50}} = {{\\int_{0}^{0.05} p^{2}(t)dt} \\over {\\int_{0}^{\\infty} p^{2}(t)dt}} $$',
            'C50 (dB)':'$$ {\\rm C_{50}} = 10 \\log_{10} ({{\\int_{0}^{0.05} p^{2}(t)dt} \\over {\\int_{0.05}^{\\infty} p^{2}(t)dt}}) $$',
            'C80 (dB)':'$$ {\\rm C_{80}} = 10 \\log_{10} ({{\\int_{0}^{0.08} p^{2}(t)dt} \\over {\\int_{0.08}^{\\infty} p^{2}(t)dt}}) $$',
        },
        tooltipText:{
            'RT60 (s)':'Reverberation time is a measure of the time required for reflecting sound to "fade away" in an enclosed area after the source of the sound has stopped. This parameter can be calculated by the extrapolation of -5 dB and -35 dB, crossing at -60 dB point.', 
            'EDT (s)':'Early Decay Time describes a subjective feeling of reverberation rather than RT60. This parameter can be calculated by the extrapolation of 0 dB and -10 dB, crossing at -60 dB point.',
            'D50':'D50 is one of the parameters that explain a speech intelligibility. D50 can be calculated by the energy ratio of the first 50 ms and the entire sequence',
            'C50 (dB)':'The parameter C means the clarity for the musical listening. C50 is the energy raito of the first 50 ms and the rest of the sequence. Its unit is decibel.',
            'C80 (dB)':'The parameter C means the clarity for the musical listening. C80 is the energy raito of the first 80 ms and the rest of the sequence. Its unit is decibel.',
        },
    }),
    props:['items','colorClass'],
    computed:{
        headers(){
            const _headers = Array.from(this.octaveBands);
            _headers.unshift({ text: 'Acoustic Parameter', value: 'parameter' });
            console.log(_headers)
            return _headers
        }
    },
}
</script>
