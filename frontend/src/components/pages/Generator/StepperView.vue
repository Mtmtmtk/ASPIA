<template>
    <v-card
        rounded="lg"
        elevation="5" 
        dark 
    >
        <v-stepper
            vertical
            v-model="stepper"
        >
            <v-stepper-step
                :complete="stepper > 1"
                step="1"
                color="#26A69A"
            >Step1: Your Recording
            </v-stepper-step>
            <v-stepper-content step="1">
                <step-one 
                    @change-step="changeStep"
                    @accept-recording-file="getReordingData"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 2"
                step="2"
                color="#26A69A"
            >Step2: Swept Sine Wave
            </v-stepper-step>
            <v-stepper-content step="2">
                <step-two 
                    @change-step="changeStep"
                    @accept-recording-file="getSweptSineData"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 3"
                step="3"
                color="#26A69A"
            >Step3: Select Space
            </v-stepper-step>
            <v-stepper-content step="3">
                <step-three 
                    @change-step="changeStep"
                    @send-space-name="determineSpace"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 4"
                step="4"
                color="#26A69A"
            >Step4: Select Position
            </v-stepper-step>
            <v-stepper-content step="4">
                <step-four
                    :duct="duct"
                    :space-name="chosenSpace"
                    @change-step="changeStep"
                    @send-abbr-audiotype-and-ir="getImpulseResponseData"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 5"
                step="5"
                color="#26A69A"
            >Step5: Select Output Channel(s)
            </v-stepper-step>
            <v-stepper-content step="5">
                <step-five
                    :ir-audio-type="IRAudioType"
                    @change-step="changeStep"
                    @emit-output-channels="callDucts"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 6"
                step="6"
                color="#26A69A"
            >Step6: Convolution
            </v-stepper-step>
            <v-stepper-content step='6'>
                <step-six
                    :space-name="chosenSpace"
                    :progress="progress"
                    @change-step="changeStep"
                />
            </v-stepper-content>

            <v-stepper-step
                :complete="stepper > 7"
                step="7"
                color="#26A69A"
            >Step7: Download
            </v-stepper-step>
            <v-stepper-content step="7">
                <step-seven :audio-url="audioURL" />
            </v-stepper-content>
        </v-stepper>
    </v-card>
</template>
<script>
import StepOne   from './StepOne.vue'
import StepTwo   from './StepTwo.vue'
import StepThree from './StepThree.vue'
import StepFour  from './StepFour.vue'
import StepFive  from './StepFive.vue'
import StepSix   from './StepSix.vue'
import StepSeven from './StepSeven.vue'

const decodeFunc = function(file,vue,target){
    const reader = new FileReader();
    const audioContext = new AudioContext();
    const postProcessFunc = function(decoded){
        let allChannelsArr = [];
        const channels = decoded.numberOfChannels;
        for(let i = 0; i < channels; i++){
            let typedArray = new Float32Array(decoded.length);
            typedArray = decoded.getChannelData(i);
            const singleArray = Array.from(typedArray);
            allChannelsArr.push(singleArray);
        }
        if(target == 'recording'){
            vue.ductsInputForm.recordingSplRate = decoded.sampleRate;
            if(allChannelsArr.length == 1) vue.ductsInputForm.recording = allChannelsArr.flat();
            else vue.ductsInputForm.recording = allChannelsArr;
        }else if(target == 'swept_sine'){
            vue.ductsInputForm.sweptSineSplRate = decoded.sampleRate;
            if(allChannelsArr.length == 1) vue.ductsInputForm.sweptSine = allChannelsArr.flat();
            else vue.ductsInputForm.sweptSine = allChannelsArr;
        }
    };
    reader.onload = function(evt) {
        const arrayBuffer = evt.target.result;
        audioContext.decodeAudioData(arrayBuffer, postProcessFunc)
    };
    reader.readAsArrayBuffer(file);
}

const encodeFunc = function(samples,samplingRate, _channels, _blockSize){
        const _buffer = new ArrayBuffer(44 + samples.length*2);
        let _view = new DataView(_buffer);
        const writeString = function(view, offset, str){
            for(let i=0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
        }
        const floatTo16BitPCM = function(output, offset, input){
            for(let i=0; i < input.length; i++, offset +=2){
                let s = Math.max(-1, Math.min(1, input[i]));
                output.setInt16(offset, s<0 ? s*0x8000 : s*0x7FFF, true);
            }
        }
        const _fileSize = 44 + samples.length*2 - 8;
        writeString(_view, 0, 'RIFF');//riff識別
        _view.setUint32(4, _fileSize, true);//chunk size
        writeString(_view, 8, 'WAVE')//format
        writeString(_view,12, 'fmt ');//fmt識別子(最後にスペース開けるのめっちゃ大事)
        _view.setUint32(16, 16, true);//fmt chunk's byte
        _view.setUint16(20,  1, true);//sound format: 1 means non-compressed linear PCM format
        _view.setUint16(22,  _channels, true);//channel(s) one or two
        _view.setUint32(24, samplingRate  , true);//sampling rate
        _view.setUint32(28, samplingRate*_blockSize, true);//sampling rate * block size
        _view.setUint16(32, _blockSize, true);//block size: channel(s) * bit/8
        _view.setUint16(34, 16, true);//bit per sample
        writeString(_view, 36, 'data');
        _view.setUint32(40, samples.length*2, true);
        floatTo16BitPCM(_view, 44, samples);
        return _view
}

export default{
    components:{
        StepOne,
        StepTwo,
        StepThree,
        StepFour,
        StepFive,
        StepSix,
        StepSeven,
    },
    data: () => ({
        stepper:1,
        chosenSpace:'',
        ductsInputForm:{
            recording:[],
            recordingSplRate:0,
            sweptSine:[],
            sweptSineSplRate:0,
            irPath:'',
            outputChannels:0
        },
        IRAudioType:'',
        convolutedAudioArr:[],
        audioURL:'',
        progress:0,
        wavHeaderInfo:{
            mono:{
                channels:1,
                blockSize:2
            },
            stereo:{
                channels:2,
                blockSize:4,
            },
            'b-format':{
                channels:4,
                blockSize:8
            }
        }
    }),
    props:['duct'],
    watch:{
        convolutedAudioArr(){
            this.audioURL = this.exportWAV(this.convolutedAudioArr)
        },
    }, 
    methods:{
        getReordingData(file){
            decodeFunc(file,this,'recording');
        },
        getSweptSineData(file){
            decodeFunc(file,this,'swept_sine');
            console.log(this.ductsInputForm);
        },
        getImpulseResponseData(...args){
            args = args.flat();
            this.IRAudioType = args[1];
            this.ductsInputForm.irPath = './impulse_response/' + args[0] + '/' + args[1] + '/' + args[2]
        },
        async callDucts(channels){
            this.ductsInputForm.outputChannels = channels;
            console.log(this.ductsInputForm.irPath)
            console.log(channels)
            console.log(this.ductsInputForm.outputChannels)
            let ret = await this.duct.call(this.duct.EVENT.EXPORT_CONVOLUTION,{
                recording: this.ductsInputForm.recording, 
                recording_spl_rate: this.ductsInputForm.recordingSplRate, 
                //swept_sine: this.ductsInputForm.sweptSine,
                //swept_sine_spl_rate: this.ductsInputForm.sweptSineSplRate,
                ir_path: this.ductsInputForm.irPath,
                output_channels: this.ductsInputForm.outputChannels,
                swept_sine: this.ductsInputForm.sweptSine,
                swept_sine_spl_rate: this.ductsInputForm.sweptSineSplRate,
            });
            this.convolutedAudioArr = ret;
            this.progress = 50;
        },
        exportWAV(audioData){
            const _dataview  = this.encodeWAV(this.mergeBuffers(audioData), this.recordingSplRate)
            const _audioBlob = new Blob([_dataview], { type: 'audio/wav' });
            let _myURL = window.URL || window.webkitURL;
            const url = _myURL.createObjectURL(_audioBlob);
            this.progress=100;
            return url
        },
        mergeBuffers(audioData){
            let _splLength = 0;
            for(let _idx = 0; _idx < audioData.length; _idx++) _splLength += audioData[_idx].length;
            let _samples = new Float32Array(_splLength);
            _samples = audioData.flat();
            let _splInd = 0;
            const channels = audioData.length;
            for(let j=0; j < audioData[0].length; j++){
                for(let i=0; i < channels; i++){
                    _samples[_splInd] = audioData[i][j];
                    _splInd++;
                }
            }
            this.progress=60
            return _samples 
        },
        encodeWAV(samples, samplingRate){
            const _channels  = this.wavHeaderInfo[this.ductsInputForm.outputChannels].channels
            const _blockSize = this.wavHeaderInfo[this.ductsInputForm.outputChannels].blockSize
            return encodeFunc(samples, samplingRate, _channels, _blockSize)
        },
        changeStep(stepVal){
            this.stepper = this.stepper + stepVal;
        },
        determineSpace(name){
            this.chosenSpace = name;
        },
    },
}
</script>
