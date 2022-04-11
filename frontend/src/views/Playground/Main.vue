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
        </v-card>
    </v-container>
</template>
<script>
import ducts from '@iflb/ducts-client'
export default{
    data:() => ({
        duct: new ducts.Duct(),
        fileName: '',
        recording: [],
        recordingSplRate: 0,
        channels: 0,
        status: ''
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
                console.log(data);
                this.status = await this.duct.call(this.duct.EVENT.SAVE_DATA_IN_REDIS, {
                    frame_no: frameNumber,
                    group_key: 'analysis',
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
        //async load(){
        //    this.ductRet = await this.duct.call(this.duct.EVENT.LOAD_DATA_FROM_REDIS, { group_key: 'hoge' });
        //    await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'hoge' });
        //    console.log(this.ductRet);
        //},
        async getAcousticParameters(){
            let irDict = {};
            [ irDict, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, {});
            this.resampledIr = Object.values(irDict);
            console.log(this.resampledIr);
            this.acousticParameters = await this.duct.call(this.duct.EVENT.ACOUSTIC_PARAMETER_GET, {
                spl_rate: this.recordingSplRate,
                filter_type: 'FIR',
                order: 5001
            });
            this.schroederDecibels = await this.duct.call(this.duct.EVENT.SCHROEDER_CURVE, {
                spl_rate: this.recordingSplRate,
                filter_type: 'FIR',
                order: 5001
            });
            await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'analysis' });
            console.log(this.acousticParameters);
            console.log(this.schroederDecibels)
        }
    },
    mounted(){
        this.duct.open("/ducts/wsd");
        console.log(this.duct)
    }
}
</script>
