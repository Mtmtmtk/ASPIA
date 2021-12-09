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
                @submit-form ='submitForm'
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
        soundArr:[],
    }),
    props:['duct'],
    methods:{
        changeStep(stepVal){
            this.stepper = stepVal;
        },
        determineSpace(name){
            this.chosenSpace = name;
        },
        updateFormContent(...args){
            this.form[args[1]] = args[0];
            console.log(args[0])
            const reader = new FileReader();
            let that = this
            reader.onloadend = function(evt) {
                console.log(evt.target.result);
                that.soundArr = new Int16Array(evt.target.result)
                console.log(that.soundArr)
            };
            reader.readAsArrayBuffer(args[0]);
        },
        submitForm(str){
            console.log(this.soundArr)
            let _sound = []
            for(let val of this.soundArr){
                _sound.push(val)
            }
            console.log(_sound)
            if(str != ''){
                this.duct.invokeOnOpen(async () => {
                    try {
                        let ret = await this.duct.call(this.duct.EVENT.CONVOLUTION,{recording: _sound, ir :''});
                        console.log(ret)
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
