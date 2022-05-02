<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        dark 
        color="#323232"
    >
        <v-row class="ps-5 pt-3">
            <v-col>
                Choose an audio whose spectrogram you want to look at .
            </v-col>
        </v-row>
        <v-card-text>
            <v-file-input
                label="Choose Audio Data"
                prepend-icon="mdi-paperclip"
                @change="getAudioData"
            >
            </v-file-input>
        </v-card-text>

        <v-card-text>
            <v-row>
                <v-col>
                    <v-btn
                        color="#26A69A"
                        :disabled="buttonDisabled"
                        :loading="loading"
                        @click="showSpectrogram"
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
        audioArray:[],
        audioSplRate:null,
        channels:null,
        timestamp:[],
        audioURL:'',
        loading: false,
        buttonDisabled: true
    }),
    props:['duct'],
    watch:{
        async audioArray(){
            this.buttonDisabled = true;
            this.loading = true;
            const audioLength = this.audioArray[0].length;
            const frameElementsNum = 44100 * 5;
            const frames = Math.ceil(audioLength/(frameElementsNum));
            for(let frameNumber = 0; frameNumber < frames; frameNumber++ ){
                const nextFrameNumber = frameNumber + 1;
                let data = [];
                if(audioLength < nextFrameNumber * (frameElementsNum))
                    data = this.audioArray.map(el => el.slice(frameNumber * frameElementsNum, audioLength + 1));
                else
                    data = this.audioArray.map(el => el.slice(frameNumber * frameElementsNum, nextFrameNumber * frameElementsNum))
                await this.duct.call(this.duct.EVENT.SAVE_DATA_IN_REDIS, {
                    frame_no: frameNumber,
                    group_key: 'spectrogram',
                    data: data,
                });
            }
            this.buttonDisabled = false;
            this.loading = false;
        }
    },
    methods:{
        async getAudioData(file){
            if(file){
                this.getFileName(file);
                await this.readAudioAsArrayBuffer(file);
                await this.readAudioAsDataURL(file);
            }else{
                this.audioArray = [];
                this.audioSplRate = null;
                this.channels = null;
            }
        },
        readAudioAsArrayBuffer(file){
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
                vue.audioArray = allChannelsArr;
                vue.audioSplRate = sampleRate;
                vue.channels = channels;
            }
            reader.onload = function(evt) {
                const arrayBuffer = evt.target.result;
                audioContext.decodeAudioData(arrayBuffer, decodedDone)
            };
            reader.readAsArrayBuffer(file);
        },
        readAudioAsDataURL(file){
            const reader = new FileReader();
            const vue = this;
            reader.onload = function(evt){ vue.audioURL = evt.target.result; };
            reader.readAsDataURL(file);
        },
        getFileName(file){
            this.fileName = file.name;
        },
        showSpectrogram(){
            this.$emit('get-audio-info', [ 
                this.audioArray, 
                this.audioSplRate, 
                this.channels, 
                this.audioURL,
                this.fileName,
            ]);
        }
    }

}
</script>
