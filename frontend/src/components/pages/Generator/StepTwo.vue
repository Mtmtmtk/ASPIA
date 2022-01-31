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
                    color='#AFB42B'
                    :href='sweptSine'
                    download
                >
                    <v-icon>mdi-download</v-icon>download
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols='6'>
                <v-file-input 
                    accept='audio/*'
                    label='File Input'
                    truncate-length='15' 
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color='#26A69A'
                    @click='continueStep'
                >Continue
                </v-btn>
                <v-btn
                    text
                    color='#8D6E63'
                    @click='cancelStep'
                >Cancel
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
export default{
    data: () => ({
        sweptSine: require('@/assets/swept_sine.wav')
    }),
    methods:{
        continueStep(){
            this.$emit('change-step', 3);
        },
        cancelStep(){
            this.$emit('change-step', 1);
        }
    }
}
</script>
