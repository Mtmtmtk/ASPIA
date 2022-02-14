<template>
    <v-container>
        <v-row>
            <v-col>
                Prepare the swept sine wave recording and register it. You can download the swept sine wave below. The positions of the sound source and receiver should be the same as Step1.
            </v-col>
        </v-row>
        <v-row>
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
        <v-row>
            <v-col cols="6">
                <v-file-input 
                    accept="audio/*"
                    label="File Input"
                    truncate-length="15" 
                />
            </v-col>
        </v-row>
        <step-changer 
            :continue-required="true"
            :continue-disabled="false"
            :cancel-required="true"
            :cancel-disabled="false"
            @change-step="changeStep"   
        />
    </v-container>
</template>
<script>
import StepChanger from '../../ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        sweptSine: require('@/assets/swept_sine.wav')
    }),
    methods:{
        changeStep(val){
            this.$emit('change-step', val);
        },
    }
}
</script>
