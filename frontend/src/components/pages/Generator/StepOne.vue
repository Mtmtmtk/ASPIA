<template>
    <v-container>
        <v-row>
            <v-col>
                Register your recording.
            </v-col>
        </v-row>
        <v-row>
            <v-col cols='6'>
                <v-file-input 
                    accept='audio/*'
                    label='File Input'
                    truncate-length='15' 
                    show-size
                    @change='emitRecordingFile'
                    :clearable='false'
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    :disabled='continueDisabled'
                    color='#26A69A'
                    @click='continueStep'
                >Continue
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
export default{
    data: () => ({
        file:'',
        continueDisabled: true
    }),
    methods:{
        continueStep(){
            this.$emit('change-step', 2);
        },
        emitRecordingFile(file){
            this.$emit('accept-recording-file', file, 'recording');
            this.continueDisabled = false;
        }
    },
    watch:{
    }
}
</script>
