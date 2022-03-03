<template>
    <div>
        <div id="wavesurfer" :style="wavesurferStyle" />
        <div id="wave-spectrogram" :style="spectrogramStyle"/>
    </div>
</template>
<script>
import WaveSurfer from 'wavesurfer.js'
import SpectrogramPlugin from 'wavesurfer.js/src/plugin/spectrogram/index.js'
import { HotColorMap } from '@/assets/color_maps/hot-color-map.js'
import { JetColorMap } from '@/assets/color_maps/jet-color-map.js'
const wavesurferStyle ={
    width: '100%'
}
const spectrogramStyle={
    width: '100%',
}

export default {
    name:"Player",
    data: () => ({
        wavesurfer:null,
        wavesurferStyle,
        spectrogramStyle,
        HotColorMap,
        JetColorMap
    }),
    props:{
        src: {
            type: String,
            default: () => ('')
        },
        currentTime: {
            type: Number,
            default: () => (0)
        },
    },
    watch:{
        currentTime(){
            this.wavesurfer.backend.media.currentTime = this.currentTime
        }
    },
    mounted(){
        this.wavesurfer = WaveSurfer.create({
            container:'#wavesurfer',
            responsive:true,
            interact:false,
            backend:'MediaElement',
            backgroundColor:'#E0E0E0',
            progressColor:'#8E24AA',
            waveColor:'#26A69A',
            plugins: [
                SpectrogramPlugin.create({
                    wavesurfer: this.wavesurfer,
                    container: "#wave-spectrogram",
                    labels: true,
                    fftSamples:1024,
                    responsive:true,
                    colorMap:JetColorMap
                })
            ]
        });
        this.wavesurfer.load(this.src)
    }
}
</script>
