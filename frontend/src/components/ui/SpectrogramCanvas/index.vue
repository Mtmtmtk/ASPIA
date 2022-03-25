<template>
    <v-row class="pb-0">
        <v-col class="pb-0" cols="1" ref="freqAxisCol">
            <canvas
                v-show="spectrogramReady"
                ref="freqAxis"
                :height="canvasHeight"
            />
        </v-col>
        <v-col class="pb-0" cols="10" sm="9" ref="spectrogramCol">
            <canvas 
                v-show="spectrogramReady"
                ref="spectrogram" 
                :height="defaultSpectrogramHeight"
            />
        </v-col>
        <v-col class="pb-0" cols="1" sm="2" ref="legendCol">
            <canvas
                v-show="spectrogramReady"
                ref="legend"
                :height="canvasHeight"
            />
        </v-col>
        <v-col class="py-0" cols="1"/>
        <v-col class="py-0" cols="10" sm="9">
            <canvas
                v-show="spectrogramReady"
                ref="timeAxis"
            />
        </v-col>
    </v-row>
</template>
<script>
import { HotColorMap } from '@/assets/color_maps/hot-color-map.js'
import { JetColorMap } from '@/assets/color_maps/jet-color-map.js'
export default{
    data:() => ({
        HotColorMap,
        JetColorMap,
        spectrogramReady:false,
        canvasHeight:300,
    }),
    props:{
        data:{
            type: Array,
            default: () => ([])
        },
        samplingPoints:{
            type: Number,
            default: () => (2048)
        },
        mode:{
            type: String,
            default: () => ('decibel')
        },
        dark:{
            type: Boolean,
            default: () => (false)
        },
        ampRange:{
            type: Array,
            default: () => ([0.1,0])
        },
        powerRange:{
            type: Array,
            default: () => ([0.1,0])
        },
        decibelRange:{
            type: Array,
            default: () => ([-10,0])
        }
    },
    computed:{
        defaultSpectrogramHeight(){
            return this.samplingPoints/2
        },
    },
    watch:{
        data(){
            this.renderAll();
        },
        decibelRange(){
            this.renderAll();
        },
        powerRange(){
            this.renderAll();
        },
        ampRange(){
            this.renderAll();
        }
    },
    methods:{
        drawSpectrogramPixel(x,y,cContext,mode,val){
            let rgba = [];
            if(mode == 'decibel'){
                const minDB = this.decibelRange[0];
                const maxDB = this.decibelRange[1];
                if(val < minDB){
                    rgba = this.JetColorMap[0];
                }else if(val > maxDB){
                    rgba = this.JetColorMap[255];
                }else{
                    let colorIdx = Math.round(val/Math.abs(maxDB + minDB)*255 + 255)
                    rgba = this.JetColorMap[colorIdx]
                }
            }else{
                let maxVal = 0;
                let minVal = 0;
                if(mode == 'power'){
                    maxVal = this.powerRange[0];
                    minVal = this.powerRange[1];
                }else if(mode == 'amp'){
                    maxVal = this.ampRange[0];
                    minVal = this.ampRange[1];
                }

                if(val > maxVal){
                    rgba = this.JetColorMap[255];
                }else if(val < minVal){
                    rgba = this.JetColorMap[0];
                }else{
                    const colorIdx = Math.round((val-minVal)/(maxVal-minVal)*255);
                    rgba = this.JetColorMap[colorIdx];
                }    
            }
            cContext.fillStyle=`rgb(${rgba[0]*255},${rgba[1]*255},${rgba[2]*255})`
            cContext.fillRect(x,y,1,1);
        },
        createSpectrogram(mode){
            if(Array.isArray(this.data) && this.data.length != 0){
                const canvas = this.$refs.spectrogram;
                canvas.width =  Math.round(this.data.length/(this.samplingPoints/2));
                const cContext = canvas.getContext('2d');
                let x = 0;
                let y = this.samplingPoints/2;
                for(let el of this.data){
                    if(y == 0){
                        y = this.samplingPoints/2;
                        x++;
                    }
                    if(mode == 'decibel'){
                        this.drawSpectrogramPixel(x,y,cContext,'decibel',el.decibel);
                    }else if(mode == 'amp'){
                        this.drawSpectrogramPixel(x,y,cContext,'amp',el.amplitude);
                    }else if(mode == 'power'){
                        this.drawSpectrogramPixel(x,y,cContext,'power',el.power);
                    }
                    y--;
                }
                canvas.style.width = `${ this.$refs.spectrogramCol.clientWidth - 32 }px`;
                canvas.style.height = '300px';
                this.spectrogramReady = true;
            }
        },
        drawLegendPixel(x,y,cContext,color){
            const rgba = color;
            cContext.fillStyle = `rgb(${rgba[0]*255},${rgba[1]*255},${rgba[2]*255})`;
            cContext.fillRect(x,y,15,2);
        },
        writeText(x,y,cContext,text,font = '16px Arial'){
            cContext.font = font;
            if(this.dark){
                cContext.fillStyle = '#FAFAFA';
            }else{
                cContext.fillStyle = '#000000';
            }
            cContext.fillText(text, x, y);
        },
        createLegend(mode){
            const canvas = this.$refs.legend;
            canvas.width = this.$refs.legendCol.clientWidth - 32;
            const cContext = canvas.getContext('2d');
            let x = 0;
            let colorIdx = 255;
            for(let el of this.JetColorMap){
                const y = Math.round(300/255 * colorIdx);
                this.drawLegendPixel(x,y,cContext,el);
                colorIdx--;
            }
            let repValues = [];
            if(mode == 'decibel'){
                const minDB = this.decibelRange[0];
                const maxDB = this.decibelRange[1];
                repValues = (maxDB == 0) ? [
                    0.0, 
                    (minDB/3).toPrecision(2), 
                    (2*minDB/3).toPrecision(2), 
                    `< ${minDB.toPrecision(2)}`
                ] : [
                    `> ${maxDB.toPrecision(2)}`, 
                    ((minDB - maxDB)/3 + maxDB).toPrecision(2), 
                    (2*(minDB-maxDB)/3 + maxDB).toPrecision(2), 
                    `< ${minDB.toPrecision(2)}`
                ];
                const yCoordineates = [14, 108, 203, 298];
                for(let idx in repValues)
                    this.writeText(20, yCoordineates[idx], cContext, repValues[idx]);
                cContext.save();
                cContext.rotate(0.5 * Math.PI);
                this.writeText(140, -30, cContext, 'dB');
                cContext.restore();
            }else{
                let maxVal = 0;
                let minVal = 0;
                if(mode == 'power'){
                    maxVal = this.powerRange[0];
                    minVal = this.powerRange[1];
                }else if(mode == 'amp'){
                    maxVal = this.ampRange[0];
                    minVal = this.ampRange[1];
                }

                if(maxVal == 1 && minVal == 0){
                    repValues = [1.0, 0.75, 0.5, 0.25, 0];
                }else{
                    if(maxVal == 1){
                        repValues = [
                            1.0, 
                            (3*(1-minVal)/4 + minVal).toPrecision(2), 
                            (  (1-minVal)/2 + minVal).toPrecision(2), 
                            (  (1-minVal)/4 + minVal).toPrecision(2), 
                            `< ${minVal.toPrecision(2)}`
                        ];
                    }else if(minVal == 0){
                        repValues = [
                            `> ${maxVal.toPrecision(2)}`, 
                            (3*maxVal/4).toPrecision(2), 
                            (maxVal/2).toPrecision(2), 
                            (maxVal/4).toPrecision(2), 
                            0.0
                        ];
                    }else{
                        repValues = [
                            `> ${maxVal.toPrecision(2)}`, 
                            (3*(maxVal-minVal)/4 + minVal).toPrecision(2), 
                            (  (maxVal-minVal)/2 + minVal).toPrecision(2), 
                            (  (maxVal-minVal)/4 + minVal).toPrecision(2), 
                            `< ${minVal.toPrecision(2)}`
                        ];
                    }
                }
                const yCoordineates = [14, 84, 155, 227, 298];
                for(let idx in repValues){
                    this.writeText(20, yCoordineates[idx], cContext, repValues[idx]);
                }
            }
        },
        createFreqAxis(){
            const canvas = this.$refs.freqAxis;
            canvas.width = this.$refs.freqAxisCol.clientWidth-8;
            const cContext = canvas.getContext('2d');
            const font = '14px Arial';
            this.writeText(canvas.width-23, 12, cContext, '22k', font);
            this.writeText(canvas.width-23, 38, cContext, '20k', font);
            this.writeText(canvas.width-23,103, cContext, '15k', font);
            this.writeText(canvas.width-23,168, cContext, '10k', font);
            this.writeText(canvas.width-16,233, cContext,  '5k', font);
            this.writeText(canvas.width-9, 298, cContext,   '0', font);
            cContext.save();
            cContext.rotate(-0.5*Math.PI);
            this.writeText(-160, canvas.width-40, cContext, 'Hz');
            cContext.restore();
        },
        createTimeAxis(){
            const canvas = this.$refs.timeAxis;
            canvas.width = this.$refs.spectrogramCol.clientWidth;
            canvas.height = 40;
            const cContext = canvas.getContext('2d');
            const font = '14px Arial';
            const endTime = this.data[this.data.length - 1].time;
            const endInt = Math.round(endTime);
            const timeStamps = [0, endInt/4, endInt/2, 3*endInt/4, endTime];
            const axisWidth = canvas.width - 50;
            let xCoordinates = [];
            timeStamps.forEach((el)=>
                xCoordinates.push(Math.round(el/endInt*axisWidth))
            );
            for(let idx in xCoordinates){
                this.writeText(xCoordinates[idx],10,cContext,timeStamps[idx],font);
            }
            this.writeText(axisWidth/2, 30, cContext, 'Time (sec)');
        },
        renderAll(){
            this.$emit('emit-current-status', 'drawing');
            this.createTimeAxis();
            this.createFreqAxis();
            this.createLegend(this.mode);
            this.createSpectrogram(this.mode);
            this.$emit('emit-current-status','finished')
        },
        downloadData(){
            const jsonData = JSON.stringify(this.data);
            const blob= new Blob([jsonData], { type:'text/plain' });
            let link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'spectrogram_data.json'
            link.click();
        }
    },
    mounted(){
        if(this.data != []) this.renderAll();
    }
}
</script>
