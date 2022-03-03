<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Spectrogram</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card dark color="#323232">
                    <v-card-text class="text-h6 pb-0">
                        Result
                    </v-card-text>
                    <v-card-text>
                        <v-wave-surfer 
                            :src="require('../recorder.wav')"
                            :current-time="currentTime"
                        />
                    </v-card-text>
                    <v-card-text class="text-body-1 py-0">
                        Control Panel
                    </v-card-text>
                    <v-card-text class="pb-7">
                        <iflb-audio-player 
                            :src="require('../recorder.wav')"
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
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import IflbAudioPlayer from "../../ui/IflbAudioPlayer.vue"
import VWaveSurfer from "../../ui/VWaveSurfer.vue"
export default{
    components: { 
        IflbAudioPlayer,
        VWaveSurfer 
    },
    data:() => ({
        currentTime:0
    }),
    props:['duct'],
    methods:{
        getCurrentTime(val){
            this.currentTime = val;
        }
    }
}
</script>
