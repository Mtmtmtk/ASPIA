<template>
    <v-card 
        rounded='lg'
        elevation='5' 
        dark 
        color='#323232'
    >
        <v-row class='ps-5 pt-3'>
            <v-col>
                Choose an impulse response you want to analyse.
            </v-col>
        </v-row>
        <v-card-text>
            <v-file-input
                label='Choose IR'
                prepend-icon='mdi-paperclip'
                @change='getIRData'
            >
            </v-file-input>
        </v-card-text>

        <v-row v-if='manualSplRateInput' class='ps-5 pt-3'>
            <v-col>
                Coundn't get a sampling rate from the file. Please enter it manually.
            </v-col>
        </v-row>
        <v-card-text v-if='manualSplRateInput'>
            <v-col cols='4'>
                <v-text-field
                    v-model='manualSplRate'
                    @blur='changeSplRate'
                    suffix='Hz'
                />
            </v-col>
        </v-card-text>

        <v-row v-if='manualChannelsInput' class='ps-5 pt-3'>
            <v-col>
                Coundn't get a number of channels from the file. Please enter it manually.
            </v-col>
        </v-row>
        <v-card-text v-if='manualChannelsInput'>
            <v-col cols='4'>
                <v-text-field
                    v-model='manualChannels'
                    @blur='changeChannels'
                />
            </v-col>
        </v-card-text>

        <v-card-text>
            <v-row>
                <v-col>
                    <v-btn
                        color='#26A69A'
                        :disabled='buttonDisbled'
                        @click='startAnalysis'
                    >
                        start analysis
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
        manualSplRateInput:false,
        manualChannelsInput:false,
        manualSplRate:0,
        manualChannels:0,
        audioURL:'',
    }),
    computed:{
        buttonDisbled(){
            if(this.recording.length != 0  && (![this.recordingSplRate,this.channels].includes(0))) return false
            else return true
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
                this.manualChannelsInput = false;
                this.manualSplRateInput = false;
            }
        },
        readIRAsArrayBuffer(file){
            console.log(file)
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
                    if(typedArray.length * channels > 44100*18){
                        singleArray = Array.from(typedArray).splice(0, 44100*18/channels);
                    }else{
                        singleArray = Array.from(typedArray);
                    }
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
        readIRAsDataURL(file){
            const reader = new FileReader();
            const vue = this;
            reader.onload = function(evt) {
                vue.audioURL = evt.target.result;
            };
            reader.readAsDataURL(file);
        },
        changeSplRate(){
            this.recordingSplRate = parseInt(this.manualSplRate);
        },
        changeChannels(){
            this.channels = parseInt(this.manualChannels);
        },
        startAnalysis(){
            this.$emit('change-component', 'ir-analysis');
            this.$emit('get-ir-info', [ 
                this.recording, 
                this.recordingSplRate, 
                this.channels, 
                this.audioURL,
                this.fileName
            ]);
        }
    }

}
</script>
