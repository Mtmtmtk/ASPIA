<template>
    <v-container>
        <v-row>
            <v-col>
                Register your anechoic (or semi-anechoic) recording. You can download it from <a :href="openAirUrl">this link</a> if you have no anechoic sound files.
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
import StepChanger from '@/components/ui/StepChanger'
export default{
    components: { StepChanger },
    data: () => ({
       file:'',
       continueDisabled: true,
       openAirUrl: 'https://www.openair.hosted.york.ac.uk/?page_id=310'

    }),
    methods: {
        changeStep(val){
            this.$emit('change-step', val);
        },
        emitRecordingFile(file){
            this.$emit('accept-recording-file', file);
            this.continueDisabled = false;
        }
    },
}
</script>
