<template>
    <v-container>
        <v-row>
            <v-col>
                Now Processing...
            </v-col>
        </v-row>
        <v-row class="my-0">
            <v-col class="pb-0">
                Status: {{ text }}
            </v-col>
        </v-row>
        <v-row class="mt-0">
            <v-col class="pt-0">
                <v-progress-linear
                    v-model="progress"
                    color="#AFB42B"
                    height="25"
                    striped
                    rounded
                >
                    <template v-slot:default="{ value }">
                        <strong>{{ Math.ceil(value) }}%</strong>
                    </template>
                </v-progress-linear>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import { library } from '../library.js'
export default{
    data: () => ({
        library,
    }),
    props:['spaceName', 'progress'],
    computed: {
        text() {
            let _text = '';
            if(this.progress == 0)        _text = 'Analysis started';
            else if(this.progress == 20)  _text = 'Importing the impulse response';
            else if(this.progress == 30)  _text = 'Sending your input data to backend';
            else if(this.progress == 40)  _text = 'Creating the anechoic sound';
            else if(this.progress == 50)  _text = 'Finished creating anechoic sound';
            else if(this.progress == 60)  _text = 'Preprocessing the impulse response and the anechoic data';
            else if(this.progress == 70)  _text = 'Executing convolution';
            else if(this.progress == 80)  _text = 'Exporting the output to the browser';
            else if(this.progress == 90)  _text = 'Encoding convoluted data as WAV';
            else if(this.progress == 100) _text = 'Processing finished!';
            return _text
        }
    },
    watch:{
        progress(){
            if(this.progress == 100)
                this.changeStep();
        },
    },
    methods:{
        changeStep(){
            this.$emit('change-step',1);
        }
    },
}
</script>
