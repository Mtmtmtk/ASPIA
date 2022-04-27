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
                <v-btn @click="getSpectrograms"
                >get spectrogram
                </v-btn>
            </v-card-text>
            <v-card-text>
                <v-card 
                    light 
                    ref="chartCard"
                    width="100%"
                    v-resize="onResize"
                >
                    <!--<v-card-title>
                        <v-row>
                            <v-col cols="6">
                                Plotly.js
                            </v-col>
                            <v-col cols="6">
                                Canvas
                            </v-col>
                        </v-row>
                    </v-card-title>
                    <v-row>
                        <v-col cols="6">
                            <div ref="sampleChart"/>
                        </v-col>
                        <v-col cols="6">
                            <spectrogram-canvas 
                                v-if="spectDb.length != 0"
                                :data="spectDb"
                                mode="decibel"
                                :decibel-range="decibelRange"
                                :sampling-points="samplingPoints"
                            />
                        </v-col>
                    </v-row>-->
                    <div ref="sampleChart"/>
                </v-card>
            </v-card-text>
        </v-card>
    </v-container>
</template>
<script>
import ducts from '@iflb/ducts-client'
import Plotly from 'plotly.js-dist-min'
//import SpectrogramCanvas from "@/components/ui/SpectrogramCanvas/index.vue"
export default{
    //components: { SpectrogramCanvas },
    data:() => ({
        duct: new ducts.Duct(),
        fileName: '',
        recording: [],
        recordingSplRate: 0,
        channels: 0,
        samplingPoints:2048,  
        spectDb: [],
        decibelRange:[-10,0],
        cardWidth: 0,
        frequencies: [],
        timestamp: [],
        zData: []
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
        onResize(){
            if(this.cardWidth != this.$refs.sampleChart.clientWidth){
                this.cardWidth = this.$refs.sampleChart.clientWidth;
                if(this.$refs.sampleChart.classList.contains('js-plotly-plot')){
                    this.relayoutChart();
                }
            }
        },
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
        async getSpectrograms(){
            //this.spectDb = await this.duct.call(this.duct.EVENT.SPECTROGRAM_DB_GET,{
            //    spl_rate: this.recordingSplRate,
            //    sampling_points: this.samplingPoints
            //});
            [ this.frequencies, this.zData, this.timestamp ] = await this.duct.call(this.duct.EVENT.PLAYGROUND,{
                spl_rate: this.recordingSplRate,
                sampling_points: this.samplingPoints
            });
            await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
            this.createChartData();
        },
        async createChartData(){
            //let frequencies = [ ...new Set(this.spectDb.map(el => el.center_frequency)) ];
            //let timestamp   = [ ...new Set(this.spectDb.map(el => el.time)) ];
            //let zDataTransposed = [];
            //timestamp.forEach(_time => {
            //    const rowData = this.spectDb.filter(el => el.time == _time).map(el => el.decibel);
            //    zDataTransposed.push(rowData);
            //});// the reason of transposing is to reduce calculation time  
            //const zData = zDataTransposed[0].map((_, col) => zDataTransposed.map(row => row[col]));
            const data = [{
                type: 'heatmap',
                //x: timestamp,
                x: this.timestamp,
                y: this.frequencies,
                z: this.zData,
                colorscale: 'Jet',
                colorbar: {
                    title: {
                        text: 'Decibel (dB)',
                        side: 'right'
                    }
                },
                zmax: 0,
                zmin: -10
            }];
            const layout = {
                title: 'Spectrogram',
                autosize: false,
                width: this.cardWidth,
                height: 500,
                margin: {
                    l: 65,
                    r: 50,
                    b: 65,
                    t: 90,
                },
                xaxis: {
                    title: {
                        text: 'Time (sec)'
                    }
                },
                yaxis: {
                    title: {
                        text: 'Frequency (Hz)'
                    }
                },
            };
            Plotly.newPlot(this.$refs.sampleChart, data, layout);
        },
        relayoutChart(){
            const update = { width: this.cardWidth };
            Plotly.relayout(this.$refs.sampleChart, update);
        },
    },
    mounted(){
        this.duct.open("/ducts/wsd");
        this.cardWidth = this.$refs.sampleChart.clientWidth
    }
}
</script>
