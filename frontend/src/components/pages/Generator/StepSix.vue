<template>
    <v-container>
        <v-row>
            <v-col>
                All done! Please download your original spatial audio.
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color='#AFB42B'
                >
                    <v-icon>mdi-download</v-icon>download
                </v-btn>
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
import { library } from '../library.js'
export default{
    data: () => ({
        library,
    }),
    props:['spaceName'],
    methods:{
        continueStep(){
            this.$emit('change-step', 1);
        },
        cancelStep(){
            this.$emit('change-step', 6);
        }
    },
}
</script>
