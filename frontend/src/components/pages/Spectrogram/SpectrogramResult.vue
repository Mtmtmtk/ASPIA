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
            <iflb-audio-player 
                :src="src"
                :is-required="{
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
            <!--<audio-chart
                :audio-arr="resampledAudio"
                :channels="channels"
                :timestamp="timestamp"
                :loading="ductCalling"
            />
            <spectrogram-canvas
                :duct="duct"
            />-->

        </v-card-text>
    </v-card>
</template>
<script>
import IflbAudioPlayer from "@/components/ui/IflbAudioPlayer.vue"
//import AudioChart from "./AudioChart"
//import SpectrogramCanvas from "@/components/ui/SpectrogramCanvas/index.vue"
import ChartTabs from "./ChartTabs"
export default{
    components: { 
        IflbAudioPlayer,
        //AudioChart,
        //SpectrogramCanvas,
        ChartTabs
    },
    data:() => ({
        currentTime:0,
    }),
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
    methods:{
        getCurrentTime(val){
            this.currentTime = val;
        }
    }
}
</script>
