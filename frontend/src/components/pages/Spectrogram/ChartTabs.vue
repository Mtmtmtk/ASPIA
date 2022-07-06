<template>
    <v-card>
        <v-tabs
            background-color="#E0E0E0"
            color="#26A69A"
            light
            show-arrows
            v-model="chartTab"
            class="rounded-t-lg"
        >
            <v-tabs-slider />
            <v-tab>raw audio</v-tab>
            <v-tab>spectrogram (decibel)</v-tab>
            <v-tab>spectrogram (power)</v-tab>
            <v-tab>spectrogram (amplitude)</v-tab>
            <v-tab>spectrogram setting</v-tab>
        </v-tabs>
        <v-tabs-items 
            v-model="chartTab"
            class="rounded-b-lg"
        >
            <v-tab-item >
                <raw-audio-chart-card
                    :current-tab="chartTab"
                    :loading="loading"
                    :audio-arr="audioArr"
                    :channels="channels"
                    :timestamp="timestamp"
                />
            </v-tab-item>
            <v-tab-item >
                <spectrogram-card 
                    mode="decibel"
                    :current-tab="chartTab"
                    :loading="loading"
                    :initial-value-range="[-80, 0]"
                    :z-data="spectDb"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item >
                <spectrogram-card 
                    mode="power"
                    :current-tab="chartTab"
                    :loading="loading"
                    :initial-value-range="[0, 0.1]"
                    :z-data="spectPow"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item >
                <spectrogram-card 
                    mode="amplitude"
                    :current-tab="chartTab"
                    :loading="loading"
                    :initial-value-range="[0, 0.1]"
                    :z-data="spectAmp"
                    :timestamp="timestamp"
                    :frequencies="frequencies"
                />
            </v-tab-item>
            <v-tab-item >
                <spectrogram-settings
                    :current-tab="chartTab"
                    :loading="loading"
                    :window-vals="windowVals"
                    @update-window-preview="onUpdateWindowPreview"
                    @update-spectrogram="onUpdateSpectrogram"
                />
            </v-tab-item>
        </v-tabs-items>
    </v-card>
</template>
<script>
import RawAudioChartCard from './RawAudioChartCard'
import SpectrogramCard from './SpectrogramCard'
import SpectrogramSettings from './Settings'
export default{
    components:{
        RawAudioChartCard,
        SpectrogramCard,
        SpectrogramSettings
    },
    data:() =>({ chartTab:'raw' }),
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
        windowVals:{
            type: Array,
            default: () => ([])
        },
    },
    methods: {
        onUpdateWindowPreview(arr){ this.$emit('update-window-preview', arr); },
        onUpdateSpectrogram(arr){ this.$emit('update-spectrogram', arr); },
    }
}
</script>
