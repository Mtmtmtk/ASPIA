<template>
    <v-card 
        rounded="lg"
        elevation="5" 
        dark 
        color="#323232"
    >
        <v-row class="ps-5 pt-3">
            <v-col v-if="!htmlText">
                {{ text }}
            </v-col>
            <v-col v-if="htmlText" v-html="text" />
        </v-row>
        <v-card-text>
            <v-file-input
                label="Choose IR"
                prepend-icon="mdi-paperclip"
                @change="getAudioData"
                accept=".mp3,audio/*"
            />
        </v-card-text>

        <v-card-text>
            <v-row>
                <v-col>
                    <v-btn
                        color="#26A69A"
                        :disabled="buttonDisabled"
                        :loading="loading"
                        @click="sendAudio"
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
        audioURL:'',
        loading: false,
        buttonDisabled: true
    }),
    props: ['duct', 'htmlText', 'groupKey', 'text'],
    methods:{
        async getAudioData(file){
            if(file){
                try {
                    this.getFileName(file);
                    await this.deleteDataInRedis();
                    await this.readAudioAsArrayBuffer(file);
                    await this.readAudioAsDataURL(file);
                }catch {
                    this.$emit('emit-loading-error')
                }
            }else{
                this.switchButtonState(true);
                this.audioArray = [];
                this.audioSplRate = null;
                this.channels = null;
            }
        },
        readAudioAsArrayBuffer(file){
            const reader = new FileReader();
            const audioContext = new AudioContext();
            const vue = this;

            const decodedDone = function(decoded){
                let allChannelsArr = [];
                for(let i = 0; i < decoded.numberOfChannels; i++){
                    let typedArray = new Float32Array(decoded.length);
                    typedArray = decoded.getChannelData(i);
                    let singleChannelArray = Array.from(typedArray);
                    allChannelsArr.push(singleChannelArray);
                }
                vue.audioArray = allChannelsArr;
                vue.audioSplRate = decoded.sampleRate;
                vue.channels= decoded.numberOfChannels
                vue.sendDataToRedis();
            }

            reader.onload = function(evt){ audioContext.decodeAudioData(evt.target.result, decodedDone) };
            reader.readAsArrayBuffer(file);
        },
        readAudioAsDataURL(file) {
            const reader = new FileReader();
            const vue = this;
            reader.onload = function(evt){ vue.audioURL = evt.target.result; };
            reader.readAsDataURL(file);
        },
        async sendDataToRedis(){
            this.switchButtonState(true);
            const audioLength = this.audioArray[0].length;
            const frameElementsNum = 44100 * 4;
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
                    group_key: this.groupKey,
                    data: data,
                });
            }
            this.switchButtonState();
        },   
        async deleteDataInRedis(){
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: this.groupKey });
            if(isKeyExists) await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: this.groupKey });
        },  
        getFileName(file){
            this.fileName = file.name;
        },
        switchButtonState(forceTrue = false){
            if(!forceTrue){
                this.buttonDisabled = !this.buttonDisabled;
                this.loading = !this.loading;
            }else{
                this.buttonDisabled = true;
                this.loading = true;
            }
        },
        sendAudio(){
            this.$emit('send-audio-info', [ 
                this.audioSplRate, 
                this.channels, 
                this.audioURL,
                this.fileName
            ]);
        },
    }

}
</script>
