<template>
    <v-container>
        <v-row v-if="!fileInputShown">
            <v-col>
                Do you want to use the swept sine wave method? If not, your recording should be recorded as anechoically as possible. If your recording place is reverberant, you had better record the swept sine wave. However, the result of convolution depends on the quality of the swept sine recording.
            </v-col>
        </v-row>
        <v-row v-if="!fileInputShown">
            <v-col>
                <v-btn
                    color="primary"
                    @click="showFileInput"
                >use
                </v-btn>
                <v-btn
                    class="ml-2"
                    color="error"
                    @click="changeStep(1)"
                >don't use
                </v-btn>
            </v-col>
        </v-row>
        <v-row v-if="fileInputShown">
            <v-col>
                Download the swept sine wave below and record it in the same place as Step1. Make sure that the positions of the sound source and receiver should be the same as Step1.
            </v-col>
        </v-row>
        <v-row v-if="fileInputShown">
            <v-col>
                <v-btn
                    color="#AFB42B"
                    :href="sweptSine"
                    download
                >
                    <v-icon>mdi-download</v-icon>download
                </v-btn>
            </v-col>
        </v-row>
        <v-row v-if="fileInputShown">
            <v-col cols="6">
                <v-file-input 
                    accept="audio/*"
                    label="File Input"
                    truncate-length="15" 
                    show-size
                    @change="emitRecordingFile"
                    :clearable="false"
                />
            </v-col>
        </v-row>
        <step-changer 
            v-if="fileInputShown"
            :continue-required="true"
            :continue-disabled="continueDisabled"
            :cancel-required="true"
            :cancel-disabled="false"
            @change-step="changeStep"   
        />
    </v-container>
</template>
<script>
import StepChanger from '@/components/ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        fileInputShown:false,
        continueDisabled:true,
        sweptSine: require('@/assets/swept_sine.wav')
    }),
    methods:{
        showFileInput(){
            this.fileInputShown = true;
        },
        changeStep(val){
            this.$emit('change-step', val);
            this.fileInputShown = (val == -1) ? false : true;
            this.continueDisabled = (val == -1) ? true : false;
        },
        emitRecordingFile(file){
            this.$emit('accept-swept-sine-file', file);
            this.continueDisabled = false;
        }
    },
}
</script>
