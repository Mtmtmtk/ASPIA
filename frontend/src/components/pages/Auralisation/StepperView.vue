<template>
    <v-card
        rounded="lg"
        elevation="5" 
        dark 
    >
        <v-stepper vertical v-model="stepper">
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
                    @get-space-name="getSpaceName"
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
                    :space-name="spaceName"
                    @change-step="changeStep"
                    @get-ir-path="getImpulseResponseData"
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
                    :ir-format="irFormat"
                    @change-step="changeStep"
                    @get-output-channels="callDucts"
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
                    :space-name="spaceName"
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
                <step-seven :audio-url="audioUrl" />
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

const decodeFunc = function(file, vue, target){
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
            vue.recordingSplRate = decoded.sampleRate;
            vue.recording = allChannelsArr;
        }else if(target == 'swept_sine'){
            vue.sweptSineSplRate = decoded.sampleRate;
            vue.sweptSine = allChannelsArr;
        }
    };
    reader.onload = function(evt) {
        const arrayBuffer = evt.target.result;
        audioContext.decodeAudioData(arrayBuffer, postProcessFunc);
    };
    reader.readAsArrayBuffer(file);
}

const encodeFunc = function(samples, samplingRate, _channels, _blockSize){
        const _buffer = new ArrayBuffer(44 + samples.length * 2);
        let _view = new DataView(_buffer);
        const writeString = function(view, offset, str){
            for(let i = 0; i < str.length; i++) view.setUint8(offset + i, str.charCodeAt(i));
        };
        const floatTo16BitPCM = function(output, offset, input){
            for(let i = 0; i < input.length; i++, offset += 2){
                let s = Math.max(-1, Math.min(1, input[i]));
                output.setInt16(offset, s<0 ? s*0x8000 : s*0x7FFF, true);
            }
        };
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

const saveDataInRedis = async function(duct, audioArr, groupKey){
    const audioLength = audioArr[0].length;
    const frameElementsNum = 44100 * 10;
    const frames = Math.ceil(audioLength/(frameElementsNum));
    for(let frameNumber = 0; frameNumber < frames; frameNumber++ ){
        const nextFrameNumber = frameNumber + 1;
        let data = [];
        if(audioLength < nextFrameNumber * (frameElementsNum))
            data = audioArr.map(el => el.slice(frameNumber * frameElementsNum, audioLength + 1));
        else
            data = audioArr.map(el => el.slice(frameNumber * frameElementsNum, nextFrameNumber * frameElementsNum))
        await duct.call(duct.EVENT.SAVE_DATA_IN_REDIS, {
            frame_no: frameNumber,
            group_key: groupKey,
            data: data,
        });
    }
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
        stepper: 1,
        recording: [],
        recordingSplRate: 0,
        sweptSine: [],
        sweptSineSplRate: 0,
        irPath: '',
        outputChannels: 0,
        spaceName: '',
        irFormat: '',
        cvAudioArr: [],
        audioUrl: '',
        progress: 0,
        wavHeaderInfo: {
            mono: {
                channels: 1,
                blockSize: 2
            },
            stereo: {
                channels: 2,
                blockSize: 4,
            },
            'b-format': {
                channels: 4,
                blockSize: 8
            }
        }
    }),
    props:['duct'],
    watch:{
        recording(){
            saveDataInRedis(this.duct, this.recording, 'convolution_recording')
        },
        sweptSine(){
            saveDataInRedis(this.duct, this.sweptSine, 'convolution_swept_sine')
        },
        async cvAudioArr(){
            this.audioUrl = this.exportWAV(this.cvAudioArr);
            await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'convolution_recording' });
            const sweptSineApplied = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: 'convolution_swept_sine' });
            if(sweptSineApplied)
                await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'convolution_swept_sine' });
        },
    }, 
    methods:{
        changeStep(stepVal){
            this.stepper = this.stepper + stepVal;
        },
        getReordingData(file){
            decodeFunc(file, this, 'recording');
        },
        getSweptSineData(file){
            decodeFunc(file, this, 'swept_sine');
        },
        getSpaceName(name){
            this.spaceName = name;
        },
        getImpulseResponseData(args){
            this.irFormat = args[1];
            this.irPath = './impulse_response/' + args[0] + '/' + args[1] + '/' + args[2];
        },
        async callDucts(channels){
            this.outputChannels = channels;
            let ret = await this.duct.call(this.duct.EVENT.EXPORT_CONVOLUTION,{
                recording_spl_rate: this.recordingSplRate, 
                swept_sine_spl_rate: this.sweptSineSplRate,
                ir_path: this.irPath,
                output_channels: this.outputChannels,
            });
            this.cvAudioArr = ret;
        },
        exportWAV(audioData){
            this.progress = 90;
            const _dataview  = this.encodeWAV(this.mergeBuffers(audioData), this.recordingSplRate);
            const _audioBlob = new Blob([_dataview], { type: 'audio/wav' });
            let _myURL = window.URL || window.webkitURL;
            const url = _myURL.createObjectURL(_audioBlob);
            this.progress = 100;
            return url
        },
        encodeWAV(samples, samplingRate){
            const _channels  = this.wavHeaderInfo[this.outputChannels].channels;
            const _blockSize = this.wavHeaderInfo[this.outputChannels].blockSize;
            return encodeFunc(samples, samplingRate, _channels, _blockSize)
        },
        mergeBuffers(audioData){
            let _splLength = 0;
            for(let _idx = 0; _idx < audioData.length; _idx++) 
                _splLength += audioData[_idx].length;
            let _samples = new Float32Array(_splLength);
            _samples = audioData.flat();
            let _splIdx = 0;
            const channels = audioData.length;
            const singleChannelLength = audioData[0].length;
            for(let j = 0; j < singleChannelLength; j++){
                for(let i = 0; i < channels; i++){
                    _samples[_splIdx] = audioData[i][j];
                    _splIdx++;
                }
            }
            return _samples 
        },
    },
    created() {
        this.duct.invokeOnOpen(() => {
            this.duct.setEventHandler(this.duct.EVENT.WATCH_STATUS, (rid, eid, status) => {
                this.progress = status;
            });
            this.duct.send(this.duct.nextRid(), this.duct.EVENT.WATCH_STATUS);
        });
    }
}
</script>
