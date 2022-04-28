<template>
    <div>
        <v-tabs
            background-color="#E0E0E0"
            color="#26A69A"
            light
            v-model="chartTab"
            class="rounded-t-lg"
        >
            <v-tab>raw audio</v-tab>
            <v-tab>spectrogram (decibel)</v-tab>
            <v-tab>spectrogram (power)</v-tab>
            <v-tab>spectrogram (amplitude)</v-tab>
        </v-tabs>
        <v-tabs-items 
            v-model="chartTab"
            class="rounded-b-lg"
        >
            <v-tab-item>
                <audio-chart-card
                    :loading="loading"
                    :audio-arr="audioArr"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-decibel-card 
                    :z-data="spectDb"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-power-card 
                    :z-data="spectPow"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-amplitude-card 
                    :z-data="spectAmp"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>
<script>
import AudioChartCard from './AudioChartCard'
import SpectrogramDecibelCard from './Spectrograms/SpectrogramDecibelCard'
import SpectrogramPowerCard from './Spectrograms/SpectrogramPowerCard'
import SpectrogramAmplitudeCard from './Spectrograms/SpectrogramAmplitudeCard'
export default{
    components:{
        AudioChartCard,
        SpectrogramDecibelCard,
        SpectrogramPowerCard,
        SpectrogramAmplitudeCard
    },
    data:() =>({
        chartTab:null,
    }),
    props:{
        loading:{
            type: Boolean,
            default: () => (true)
        },
        audioArr:{
            type: Array,
            default: () => ([])
        },
        channels: {
            type: Number,
            default: 0
        },
        frequencies:{
            type: Array,
            default: () => ([])
        },
        timestamp:{
            type: Array,
            default: () => ([])
        },
        spectDb:{
            type: Array,
            default: () => ([])
        },
        spectPow:{
            type: Array,
            default: () => ([])
        },
        spectAmp:{
            type: Array,
            default: () => ([])
        },
    },
}
</script>
