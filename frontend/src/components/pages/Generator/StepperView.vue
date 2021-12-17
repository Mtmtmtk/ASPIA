<template>
    <v-card
        rounded='lg'
        elevation='5' 
        dark 
    >
        <v-stepper
            vertical
            v-model='stepper'
        >
        <v-stepper-step
            :complete='stepper > 1'
            step='1'
            color='#26A69A'
        >Step1: Your Recording
        </v-stepper-step>
        <v-stepper-content step='1'>
            <step-one 
                @change-step='changeStep'
                @accept-recording-file='updateFormContent'
            />
        </v-stepper-content>

        <v-stepper-step
            :complete='stepper > 2'
            step='2'
            color='#26A69A'
        >Step2: Swept Sine Wave
        </v-stepper-step>
        <v-stepper-content step='2'>
            <step-two 
                @change-step='changeStep'
            />
        </v-stepper-content>

        <v-stepper-step
            :complete='stepper > 3'
            step='3'
            color='#26A69A'
        >Step3: Select Space
        </v-stepper-step>
        <v-stepper-content step='3'>
            <step-three 
                @change-step='changeStep'
                @send-space-name='determineSpace'
            />
        </v-stepper-content>

        <v-stepper-step
            :complete='stepper > 4'
            step='4'
            color='#26A69A'
        >Step4: Select Position
        </v-stepper-step>
        <v-stepper-content step='4'>
            <step-four
                :spaceName='chosenSpace'
                @change-step='changeStep'
                @send-IR-name ='submitForm'
            />
        </v-stepper-content>

        <v-stepper-step
            :complete='stepper > 5'
            step='5'
            color='#26A69A'
        >Step5: Convolution
        </v-stepper-step>
        <v-stepper-content step='5'>
            <step-five
                :spaceName='chosenSpace'
                @change-step='changeStep'
                :progress='progress'
            />
        </v-stepper-content>

        <v-stepper-step
            :complete='stepper > 6'
            step='6'
            color='#26A69A'
        >Step6: Download
        </v-stepper-step>
        <v-stepper-content step='6'>
            <step-six
                :audioURL='audioURL'
                @change-step='changeStep'
            />
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
import StepSix  from './StepSix.vue'

export default{
    components:{
        StepOne,
        StepTwo,
        StepThree,
        StepFour,
        StepFive,
        StepSix
    },
    data: () => ({
        stepper:1,
        form:{},
        chosenSpace:'',
        recording:[],
        recordingSplRate: null,
        convolutedAudioArr:[],
        audioURL:{},
        progress:0,
    }),
    props:['duct'],
    watch:{
        convolutedAudioArr(){
            this.audioURL = this.exportWAV(this.convolutedAudioArr)
            console.log(this.audioURL)
        }
    }, 
    methods:{
        exportWAV(audioData){
            const _dataview  = this.encodeWAV(this.mergeBuffers(audioData), this.recordingSplRate)
            this.progress=70
            const _audioBlob = new Blob([_dataview], { type: 'audio/wav' });
            let _myURL = window.URL || window.webkitURL;
            console.log(_myURL)
            const url = _myURL.createObjectURL(_audioBlob);
            this.progress=100
            return url
        },
        mergeBuffers(audioData){//audioDataを一次元に変換してるArray.flat()でよくない？
            let _splLength = 0;
            for(let _ind = 0; _ind < audioData.length; _ind++) _splLength += audioData[_ind].length;
            let _samples = new Float32Array(_splLength)
            _samples = audioData.flat();
            let _splInd = 0;
            for(let j=0; j < audioData[0].length; j++){
                for(let i=0; i < audioData.length; i++){
                    _samples[_splInd] = audioData[i][j];
                    _splInd++;
                }
            }
            this.progress=60
            return _samples 
        },
        encodeWAV(samples, samplingRate){
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
            console.log(samplingRate)
            writeString(_view, 0, 'RIFF');//riff識別子 ok
            _view.setUint32(4, 44 + samples.length*2 - 8, true);//chunk size
            writeString(_view, 8, 'WAVE')//format ok
            writeString(_view,12, 'fmt ');//fmt識別子(最後にスペース開けるのめっちゃ大事) ok
            _view.setUint32(16, 16, true);//fmt chunk's byte ok
            _view.setUint16(20,  1, true);//sound format: 1 means non-compressed linear PCM format ok
            _view.setUint16(22,  2, true);//channel(s) one or two ok
            _view.setUint32(24, samplingRate  , true);//sampling rate ok
            _view.setUint32(28, samplingRate*4, true);//sampling rate * block size ok
            _view.setUint16(32,  4, true);//block size: channel(s) * bit/8 ok
            _view.setUint16(34, 16, true);//bit per sample ok
            writeString(_view, 36, 'data'); //ok
            _view.setUint32(40, samples.length*2, true);
            floatTo16BitPCM(_view, 44, samples);

            console.log(_view)
            return _view
        },
        changeStep(stepVal){
            this.stepper = stepVal;
        },
        determineSpace(name){
            this.chosenSpace = name;
        },
        updateFormContent(...args){
            this.form[args[1]] = args[0];
            const reader = new FileReader();
            let that = this
            reader.onloadend = function(evt) {
                console.log(evt.target.result)
                that.recording = Array.from(new Int16Array(evt.target.result));
                const view = new DataView(evt.target.result)
                that.recordingSplRate = view.getUint32(24, true)
            };
            reader.readAsArrayBuffer(args[0]);
        },
        submitForm(IRName){
            if(IRName != ''){
                console.log('hakka');
                this.duct.invokeOnOpen(async () => {
                    try {
                        let ret = await this.duct.call(this.duct.EVENT.CONVOLUTION,{
                            recording: this.recording, 
                            sampling_rate: this.recordingSplRate, 
                            ir: IRName
                        });
                        this.convolutedAudioArr = ret;
                        console.log(this.convolutedAudioArr);
                        this.progress = 50;
                    }catch{
                        console.error()
                    }
                })
            }
        }
    },

    created(){
    }
}
</script>
