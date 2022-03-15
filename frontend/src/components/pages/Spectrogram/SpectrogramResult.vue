<template>
    <v-card dark color="#323232">
        <v-card-text class="text-h6 pb-0">
            Result
        </v-card-text>
        <v-card-text>
            <!--<v-wave-surfer 
                :src="src"
                :current-time="currentTime"
            />-->
            <audio-chart
                :audio-arr="resampledAudio"
                :channels="channels"
                :timestamp="timestamp"
                :loading="ductCalling"
            />
            <spectrogram-canvas
                :analyser-node="analyserNode"
            />
        </v-card-text>
        <v-card-text class="text-body-1 py-0">
            Control Panel
        </v-card-text>
        <v-card-text class="pb-7">
            <iflb-audio-player 
                :src="src"
                :is-required="{
                    fastForward:false,
                    rewind:false,
                    skipBackward:false,
                    skipForward:false,
                    downloadIcon:false,
                    playbackSpeedIcon:false
                }"
                @get-current-time="getCurrentTime"
            />
        </v-card-text>
    </v-card>
</template>
<script>
import IflbAudioPlayer from "@/components/ui/IflbAudioPlayer.vue"
import AudioChart from "./AudioChart"
//import VWaveSurfer from "@/components/ui/VWaveSurfer.vue"
import SpectrogramCanvas from "@/components/ui/SpectrogramCanvas"
export default{
    components: { 
        IflbAudioPlayer,
        //VWaveSurfer,
        AudioChart,
        SpectrogramCanvas
    },
    data:() => ({
        currentTime:0,
    }),
    props:['duct','src','analyserNode','resampledAudio','channels','ductCalling','timestamp'],
    methods:{
        getCurrentTime(val){
            this.currentTime = val;
        }
    }
}
</script>
