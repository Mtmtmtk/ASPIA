<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        color="#323232"
        dark
    >
        <v-card-title>Result / {{ fileName }}</v-card-title>
        <v-card-text>
            <v-row>
                <v-col class="text-body-1">
                    Audio Player
                </v-col>
            </v-row>
            <v-audio 
                :src="src"
                :display-flags="{
                    skipBackward:false,
                    skipForward:false,
                    downloadIcon:false,
                    playbackSpeedIcon:false
                }"
            />
        </v-card-text>
        <v-card-text>
            <chart-tabs 
                :loading="loading"
                :audio-arr="resampledAudio"
                :frequencies="frequencies"
                :timestamp="timestamp"
                :channels="channels"
                :spect-db="spectDb"
                :spect-pow="spectPow"
                :spect-amp="spectAmp"
                :window-vals="windowVals"
                @update-window-preview="onUpdateWindowPreview"
                @update-spectrogram="onUpdateSpectrogram"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import VAudio from "@/components/ui/VAudio"
import ChartTabs from "./ChartTabs"
export default{
    components: { 
        VAudio,
        ChartTabs
    },
    props:[
        'src',
        'fileName',
        'resampledAudio',
        'channels',
        'timestamp',
        'frequencies',
        'spectDb',
        'spectPow',
        'spectAmp',
        'windowVals',
        'loading',
    ],
    methods: {
        onUpdateWindowPreview(arr) { this.$emit('update-window-preview', arr); },
        onUpdateSpectrogram() { this.$emit('update-spectrogram'); },
    }
}
</script>
