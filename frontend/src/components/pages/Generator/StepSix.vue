<template>
    <v-container>
        <v-row>
            <v-col>
                Now Processing... Please wait for a while.
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-progress-linear
                    v-model='progress'
                    color='#AFB42B'
                    height='25'
                    striped
                    rounded
                >
                    <template v-slot:default='{ value }'>
                        <strong>{{ Math.ceil(value) }}%</strong>
                    </template>
                </v-progress-linear>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color='primary'
                >test progress
                </v-btn>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
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
    props:['spaceName','progress'],
    methods:{
        continueStep(){
            this.$emit('change-step', 7);
        },
        cancelStep(){
            this.$emit('change-step', 5);
        }
    },
    watch:{
        progress(){
            if(this.progress == 100)this.continueStep();
        },
    }
}
</script>
