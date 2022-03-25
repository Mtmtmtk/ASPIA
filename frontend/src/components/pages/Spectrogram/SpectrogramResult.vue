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
                :loading="ductCalling"
                :audio-arr="resampledAudio"
                :channels="channels"
                :timestamp="timestamp"
                :sampling-points="samplingPoints"
                :spect-db="spectDb"
                :spect-pow="spectPow"
                :spect-amp="spectAmp"
                :duct="duct"
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
        'duct',
        'src',
        'fileName',
        'resampledAudio',
        'channels',
        'timestamp',
        'samplingPoints',
        'spectDb',
        'spectPow',
        'spectAmp',
        'ductCalling',
    ],
}
</script>
