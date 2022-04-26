<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Playground</font>
            </v-col>
        </v-row>
        <v-card dark>
            <v-row class="ps-5 pt-3">
                <v-col>
                    Choose an impulse response you want to analyse.
                </v-col>
            </v-row>
            <v-card-text>
                <v-file-input
                    label="Choose IR"
                    prepend-icon="mdi-paperclip"
                    @change="getIRData"
                >
                </v-file-input>
            </v-card-text>
            <v-btn @click="getAcousticParameters"
            >get Acoustic Parameters
            </v-btn>
            <div ref="sampleChart"/>
            <spectrogram-canvas 
                v-if="spectDb.length != 0"
                :data="spectDb"
                mode="decibel"
                :decibel-range="decibelRange"
                :sampling-points="samplingPoints"
            />
        </v-card>
    </v-container>
</template>
<script>
import ducts from '@iflb/ducts-client'
import Plotly from 'plotly.js-dist-min'
import SpectrogramCanvas from "@/components/ui/SpectrogramCanvas/index.vue"
export default{
    components: { SpectrogramCanvas },
    data:() => ({
        duct: new ducts.Duct(),
        fileName: '',
        recording: [],
        recordingSplRate: 0,
        channels: 0,
        samplingPoints:2048,  
        spectDb: [],
        decibelRange:[-10,0]
    }),
    watch:{
        async recording(){
            const audioLength = this.recording[0].length;
            const frameElementsNum = 44100 * 10;
            const frames = Math.ceil(audioLength/(frameElementsNum));
            for(let frameNumber = 0; frameNumber < frames; frameNumber++ ){
                const nextFrameNumber = frameNumber + 1;
                let data = [];
                if(audioLength < nextFrameNumber * (frameElementsNum))
                    data = this.recording.map(el => el.slice(frameNumber * frameElementsNum, audioLength + 1));
                else
                    data = this.recording.map(el => el.slice(frameNumber * frameElementsNum, nextFrameNumber * frameElementsNum))
                this.status = await this.duct.call(this.duct.EVENT.SAVE_DATA_IN_REDIS, {
                    frame_no: frameNumber,
                    group_key: 'spectrogram',
                    data: data,
                });
            }
        }   
    }, 
    methods:{
        async getIRData(file){
            if(file)
                await this.readIRAsArrayBuffer(file);
        },
        readIRAsArrayBuffer(file){
            this.fileName = file.name;
            const reader = new FileReader();
            const audioContext = new AudioContext();
            const vue = this;
            const decodedDone = function(decoded){
                const sampleRate = decoded.sampleRate;
                const channels = decoded.numberOfChannels;
                const allChannelsArr = [];
                for(let i = 0; i < channels; i++){
                    let typedArray = new Float32Array(decoded.length);
                    typedArray = decoded.getChannelData(i);
                    let singleArray = [];
                    singleArray = Array.from(typedArray);
                    allChannelsArr.push(singleArray);
                }
                vue.recording = allChannelsArr;
                vue.recordingSplRate = sampleRate;
                vue.channels = channels;
            }
            reader.onload = function(evt) {
                const arrayBuffer = evt.target.result;
                audioContext.decodeAudioData(arrayBuffer, decodedDone)
            };
            reader.readAsArrayBuffer(file);
        },
        async getAcousticParameters(){
            this.spectDb = await this.duct.call(this.duct.EVENT.SPECTROGRAM_DB_GET,{
                spl_rate: this.recordingSplRate,
                sampling_points: this.samplingPoints
            });
            console.log(this.spectDb)
            await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
            this.createChartData();
        },
        createChartData(){
            let timestamp = [ ...new Set(this.spectDb.map(el => el.time)) ];
            let zData = [];
            for(let _time of timestamp){
                const rowData = this.spectDb.filter(el => el.time == _time).map(el => el.decibel);
                zData.push(rowData);
            }
            const data = [{
                z: zData,
                type: 'surface'
            }];
            const layout = {
                title: 'Spectrogram',
                autosize: false,
                width: 500,
                height: 500,
                margin: {
                    l: 65,
                    r: 50,
                    b: 65,
                    t: 90,
                }
            };
            console.log(zData);
            Plotly.newPlot(this.$refs.sampleChart, data, layout);
        }
    },
    mounted(){
        this.duct.open("/ducts/wsd");
        console.log(Plotly);
    }
}
</script>
