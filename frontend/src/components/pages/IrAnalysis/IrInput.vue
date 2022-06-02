<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        dark 
        color="#323232"
    >
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
        <v-card-text>
            <v-row>
                <v-col>
                    <v-btn
                        color="#26A69A"
                        :disabled="buttonDisbled"
                        @click="startAnalysis"
                    >start analysis
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
export default{
    data:() => ({
        fileName:'',
        recording:[],
        recordingSplRate:null,
        channels:null,
        timestamp:[],
        audioURL:'',
    }),
    props: ["duct"],
    computed:{
        buttonDisbled(){
            if(this.recording.length != 0  && (![this.recordingSplRate,this.channels].includes(0))) return false
            else return true
        }
    },
    watch: {
        async recording() {
            const audioLength = this.recording[0].length;
            const frameElementsNum = 44100 * 4;
            const frames = Math.ceil(audioLength/(frameElementsNum));
            for(let frameNumber = 0; frameNumber < frames; frameNumber++ ){
                const nextFrameNumber = frameNumber + 1;
                let data = [];
                if(audioLength < nextFrameNumber * (frameElementsNum))
                    data = this.recording.map(el => el.slice(frameNumber * frameElementsNum, audioLength + 1));
                else
                    data = this.recording.map(el => el.slice(frameNumber * frameElementsNum, nextFrameNumber * frameElementsNum))

                await this.duct.call(this.duct.EVENT.SAVE_DATA_IN_REDIS, {
                    frame_no: frameNumber,
                    group_key: 'analysis',
                    data: data,
                });
            }
        }
    },
    methods:{
        async getIRData(file){
            if(file){
                await this.readIRAsArrayBuffer(file);
                await this.readIRAsDataURL(file);
            }else{
                this.recording = [];
                this.recordingSplRate = null;
                this.channels = null;
            }
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
                    let singleChannelArray = Array.from(typedArray);
                    allChannelsArr.push(singleChannelArray);
                }
                vue.recording = allChannelsArr;
                vue.recordingSplRate = sampleRate;
                vue.channels = channels;
            }
            reader.onload = function(evt){ audioContext.decodeAudioData(evt.targert.result, decodedDone) };
            reader.readAsArrayBuffer(file);
        },
        readIRAsDataURL(file){
            const reader = new FileReader();
            const vue = this;
            reader.onload = function(evt){ vue.audioURL = evt.target.result; };
            reader.readAsDataURL(file);
        },
        startAnalysis(){
            this.$emit('get-ir-info', [ 
                this.recording, 
                this.recordingSplRate, 
                this.channels, 
                this.audioURL,
                this.fileName
            ]);
        },
    }

}
</script>
