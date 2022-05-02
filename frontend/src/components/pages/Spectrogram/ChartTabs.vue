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
                <raw-audio-chart-card
                    :loading="loading"
                    :audio-arr="audioArr"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-card 
                    mode="decibel"
                    :initial-value-range="[0, -10]"
                    :loading="loading"
                    :z-data="spectDb"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-card 
                    mode="power"
                    :initial-value-range="[0.1, 0]"
                    :loading="loading"
                    :z-data="spectPow"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item>
                <spectrogram-card 
                    mode="amplitude"
                    :initial-value-range="[0.1, 0]"
                    :loading="loading"
                    :z-data="spectAmp"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
        </v-tabs-items>
    </div>
</template>
<script>
import RawAudioChartCard from './RawAudioChartCard'
import SpectrogramCard from './SpectrogramCard'
export default{
    components:{
        RawAudioChartCard,
        SpectrogramCard,
    },
    data:() =>({ chartTab:null }),
    props:{
        loading:{
            type: Boolean,
            default: true
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
