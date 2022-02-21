<template>
    <v-container>
        <v-row>
            <v-col>
                Register your recording. (Current acceptable format: monoral .wav)
            </v-col>
        </v-row>
        <v-row>
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
            :continue-required="true"
            :continue-disabled="continueDisabled"
            :cancel-required="false"
            @change-step="changeStep"   
        />
    </v-container>
</template>
<script>
import StepChanger from '../../ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        file:'',
        continueDisabled: true
    }),
    methods:{
        changeStep(val){
            this.$emit('change-step', val);
        },
        emitRecordingFile(file){
            console.log(file);
            this.$emit('accept-recording-file', file, 'recording');
            this.continueDisabled = false;
        }
    },
}
</script>
