<template>
    <div>
        <canvas ref="canvas" width="640" height="480" />
    </div>
</template>
<script>
import { HotColorMap } from '@/assets/color_maps/hot-color-map.js'
import { JetColorMap } from '@/assets/color_maps/jet-color-map.js'

//const feedSpectrogram = function(canvas,canvasContext, analyserNode, colorMap){
//    canvasContext.drawImage(canvas, -1, 0);
//
//    const freqData = new Uint8Array(this.analyserNode.frequencyBinCount);
//    analyserNode.getByteFrequencyData(freqData);
//    for(let idx=0; idx < canvas.height; idx++){
//        if(i < freqData.length) canvasContext.fillStyle = colorMap[freqData[i]];
//        else canvasContext.fillStyle = colorMap[0];
//        canvasContext.fillRect(canvas.width - 1, canvas.height - 1 - i, 1, 1);
//    }
//}

export default{
    data:()=>({
        HotColorMap,
        JetColorMap
    }),
    props:['analyserNode'],
    mounted(){
        console.log(this.analyserNode);
        //const canvas = this.$refs.canvas;
        //const canvasContext = canvas.getContext('2d')
        //this.analyserNode.smoothingTimeConstant=0;
        //this.analyserNode.fftSize=2048;
        //const freqData = new Uint8Array(this.analyserNode.frequencyBinCount);
        //this.analyserNode.getByteFrequencyData(freqData);
    }
}
</script>
