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
                color="#424242"
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
            'RT60 (s)': '$$ {\\rm RT_{60}} = {11 \\over 6} T_{-35} - {5 \\over 6} T_{-5} \\ \\mathrm{seconds} $$',
            'EDT (s)':'$$ {\\rm EDT} = 6 T_{-10} \\ \\mathrm{seconds} $$',
            'D50':'$$ {\\rm D_{50}} = {{\\int_{0}^{0.05} p^{2}(t)dt} \\over {\\int_{0}^{\\infty} p^{2}(t)dt}} $$',
            'C50 (dB)':'$$ {\\rm C_{50}} = 10 \\log_{10} ({{\\int_{0}^{0.05} p^{2}(t)dt} \\over {\\int_{0.05}^{\\infty} p^{2}(t)dt}}) = 10 \\log{(\\frac{D_{50}}{1-D_{50}})} \\ \\mathrm{dB} $$',
            'C80 (dB)':'$$ {\\rm C_{80}} = 10 \\log_{10} ({{\\int_{0}^{0.08} p^{2}(t)dt} \\over {\\int_{0.08}^{\\infty} p^{2}(t)dt}}) \\ \\mathrm{dB}$$',
            'Ts (s)': '$$ {\\rm T_s} = {{\\int_{0}^{\\infty} tp^{2}(t)dt} \\over {\\int_{0}^{\\infty} p^{2}(t)dt}} \\ \\mathrm{seconds}$$'
        },
        tooltipText:{
            'RT60 (s)': 'RT60 is a reverberation time that quantify how reverberant the space is. This parameter is ideally the time it takes for the impulse response to decay by 60 dB, but the correct value may not be obtained due to receiver performance. In such cases, it is determined by the time taken for the straight line passing through -5 dB and -35 dB of the Schröder curve to reach -60 dB. Nebraska Acoustics Group says good concert halls have a reverberation time between 1.8 and 2.2 seconds at mid-frequencies.',
            'EDT (s)': 'Early Decay Time represents a more subjective reverberation than RT60. It is determined by the time taken for the straight line passing through 0 dB and -10 dB of the Schröder curve to reach -60 dB. According to ISO:3382-1, the typical range of this value for non-occupied concert hall is between 1.0 and 3.0 seconds at mid-frequencies.',
            'D50': 'D50 is one of the parameters that explain the speech intelligibility. D50 can be calculated by the energy ratio of the first 50 ms and the entire sequence. The typical range is between 0.3 to 0.7 according to ISO:3382-1.',
            'C50 (dB)': 'C50 is one of the parameters that explain the speech intelligibility. C50 is the energy raito of the first 50 ms and the rest of the sequence, whose unit is decibel. This value is compatible with D50; its typical range is betweeen -3.68 to +3.68 dB.',
            'C80 (dB)': 'The parameter C80 describes the clarity for the musical listening. C80 is the energy raito of the first 80 ms and the rest of the sequence, whose unit is decibel. ISO:3392-1 says its typical range for concert halls is between -5 to +5 dB. However, Nebraska Acoustics Group says the acceptable values for C80(3), the average of C80 values at 500 Hz, 1kHz, and 2kHz, are between -4 and +1 dB for concert halls.',
            'Ts (s)': 'Centre Time (Ts) is the time of the centre of gravity of the squared impulse response, which typical range for the concert hall is between 60 ms and 260 ms. This parameter also relates to the perceived clarity.'
        },
    }),
    props:['items','colorClass'],
    computed:{
        headers(){
            const _headers = Array.from(this.octaveBands);
            _headers.unshift({ text: 'Acoustic Parameter', value: 'parameter' });
            return _headers
        }
    },
}
</script>

