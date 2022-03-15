<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Playground</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <v-card :color="cardColor">
                    <v-row class="pb-0">
                        <v-col class="pb-0" cols="1" ref="freqAxisCol">
                            <canvas
                                v-show="spectrogramReady"
                                ref="freqAxis"
                                :height="canvasHeight"
                            />
                        </v-col>
                        <v-col class="pb-0" cols="10" ref="spectrogramCol">
                            <canvas 
                                v-show="spectrogramReady"
                                ref="spectrogram" 
                                :height="defaultSpectrogramHeight"
                            />
                        </v-col>
                        <v-col class="pb-0" cols="1" ref="legendCol">
                            <canvas
                                v-show="spectrogramReady"
                                ref="legend"
                                :height="canvasHeight"
                            />
                        </v-col>
                        <v-col class="py-0" cols="1"/>
                        <v-col class="py-0" cols="10">
                            <canvas
                                v-show="spectrogramReady"
                                ref="timeAxis"
                            />
                        </v-col>
                    </v-row>
                    <!--<v-row v-if="spectrogramReady">
                        <v-col class="mr-4 pt-0 d-flex justify-end">
                            <v-btn
                                dark
                                color="#26A69A"
                                @click="downloadData"
                            ><v-icon>mdi-download</v-icon>download data
                            </v-btn>
                        </v-col>
                    </v-row>-->
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import ducts from '@iflb/ducts-client'
import { HotColorMap } from '../../assets/color_maps/hot-color-map.js'
import { JetColorMap } from '../../assets/color_maps/jet-color-map.js'
export default{
    data:() => ({
        HotColorMap,
        JetColorMap,
        duct: new ducts.Duct(),
        ductRet:[],
        spectrogramReady:false,
        samplingPoints:1024,
        canvasHeight:300,
    }),
    props:{
        mode:{
            type: String,
            default: () => ('decibel')
        },
        dark:{
            type: Boolean,
            default: () => (true)
        },
        maxAmp:{
            type: Number,
            default: () => (0.1)
        },
        maxPower:{
            type: Number,
            default: () => (0.1)
        },
        minDB: {
            type: Number,
            default: () => (-10)
        }
    },
    computed:{
        cardColor(){
            if(this.dark) return '#212121'
            else return '#FFFFFF'
        },
        defaultSpectrogramHeight(){
            return this.samplingPoints/2
        },
    },
    watch:{
        ductRet(){
            this.createTimeAxis();
            this.createFreqAxis();
            this.createLegend(this.mode);
            this.createSpectrogram(this.mode);
        }  
    }, 
    methods:{
        drawSpectrogramPixel(x,y,cContext,mode,val){
            let rgba = [];
            if(mode == 'amp'){
                if(val > this.maxAmp){
                    rgba = this.JetColorMap[255];
                }else{
                    const colorIdx = Math.round(val/this.maxAmp*255);
                    rgba = this.JetColorMap[colorIdx];
                }    
            }else if(mode == 'decibel'){
                if(val < this.minDB){
                    rgba = this.JetColorMap[0];
                }else{
                    let colorIdx = Math.round(val/Math.abs(this.minDB)*255 + 255)
                    rgba = this.JetColorMap[colorIdx]
                }
            }else if(mode == 'power'){
                if(val > this.maxPower){
                    rgba = this.JetColorMap[255];
                }else{
                    const colorIdx = Math.round(val/this.maxPower*255);
                    rgba = this.JetColorMap[colorIdx];
                }    
            }
            cContext.fillStyle=`rgb(${rgba[0]*255},${rgba[1]*255},${rgba[2]*255})`
            cContext.fillRect(x,y,1,1);
        },
        createSpectrogram(mode){
            if(Array.isArray(this.ductRet) && this.ductRet.length != 0){
                const canvas = this.$refs.spectrogram;
                canvas.width =  Math.round(this.ductRet.length/(this.samplingPoints/2));
                const cContext = canvas.getContext('2d');
                let x = 0;
                let y = this.samplingPoints/2;
                for(let el of this.ductRet){
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
                repValues = [0.0, (this.minDB/3).toPrecision(2), (2*this.minDB/3).toPrecision(2), `< ${this.minDB.toPrecision(2)}`];
                const yCoordineates = [14, 108, 203, 298];
                for(let idx in repValues){
                    this.writeText(20, yCoordineates[idx], cContext, repValues[idx]);
                }
                cContext.save();
                cContext.rotate(0.5 * Math.PI);
                this.writeText(140, -30, cContext, 'dB');
                cContext.restore();
            }else if(mode == 'amp'){
                if(this.maxAmp == 1){
                    repValues = [this.maxAmp.toPrecision(2), (3*this.maxAmp/4).toPrecision(2), (this.maxAmp/2).toPrecision(2), (this.maxAmp/4).toPrecision(2), 0.0];
                }else{
                    repValues = [`> ${this.maxAmp.toPrecision(2)}`, (3*this.maxAmp/4).toPrecision(2), (this.maxAmp/2).toPrecision(2), (this.maxAmp/4).toPrecision(2), 0.0];
                }
                const yCoordineates = [14, 84, 155, 227, 298];
                for(let idx in repValues){
                    this.writeText(20, yCoordineates[idx], cContext, repValues[idx]);
                }
            }else if(mode == 'power'){
                if(this.maxAmp == 1){
                    repValues = [this.maxPower.toPrecision(2), (3*this.maxPower/4).toPrecision(2), (this.maxPower/2).toPrecision(2), (this.maxPower/4).toPrecision(2), 0.0];
                }else{
                    repValues = [`> ${this.maxPower.toPrecision(2)}`, (3*this.maxPower/4).toPrecision(2), (this.maxPower/2).toPrecision(2), (this.maxPower/4).toPrecision(2), 0.0];
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
            const endTime = this.ductRet[this.ductRet.length - 1].time;
            const endInt = Math.round(endTime);
            const timeStamps = [0, endInt/4, endInt/2, 3*endInt/4, endTime];
            const axisWidth = canvas.width - 50;
            let xCoordinates = [];
            timeStamps.forEach((el)=>
                xCoordinates.push(Math.round(el/endInt*axisWidth))
            );
            console.log(xCoordinates);
            for(let idx in xCoordinates){
                console.log(idx)
                this.writeText(xCoordinates[idx],10,cContext,timeStamps[idx],font);
            }
            this.writeText(axisWidth/2, 30, cContext, 'Time (sec)');
        },
        downloadData(){
            const jsonData = JSON.stringify(this.ductRet);
            const blob= new Blob([jsonData], { type:'text/plain' });
            let link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'spectrogram_data.json'
            link.click();
        }
    },
    mounted(){
        this.duct.open("/ducts/wsd");
        this.duct.invokeOnOpen(async () => {
            if(this.mode == 'decibel'){
                this.ductRet = await this.duct.call(this.duct.EVENT.SPECTROGRAM_DB_GET,{
                    sampling_points: this.samplingPoints
                });
            }else if(this.mode == 'amp'){
                this.ductRet = await this.duct.call(this.duct.EVENT.SPECTROGRAM_AMP_GET,{
                    sampling_points: this.samplingPoints
                });
            }else if(this.mode == 'power'){
                console.log('hoge')
                this.ductRet = await this.duct.call(this.duct.EVENT.SPECTROGRAM_POWER_GET,{
                    sampling_points: this.samplingPoints
                });
            }
            console.log(this.duct.EVENT.SPECTROGRAM_POWER_GET)
        });
    }
}
</script>
