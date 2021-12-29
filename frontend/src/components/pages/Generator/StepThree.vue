<template>
    <v-container>
        <v-row>
            <v-col cols='3' 
                v-for='hall in library' 
                :key='hall.name'
            >
                <v-card 
                    rounded='lg'
                    elevation='5'
                    @click='emitSpaceName(hall.name)'
                >
                    <v-img
                        :src=hall.image
                        class="white--text"
                        :aspect-ratio='4/3'
                        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
                    >
                        <v-responsive :aspect-ratio='4/3' class='align-end'>
                            <v-card-text>{{ hall.name }}</v-card-text>
                        </v-responsive>
                    </v-img>
                </v-card>
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
        library
    }),
    methods:{
        continueStep(){
            this.$emit('change-step', 4);
        },
        cancelStep(){
            this.$emit('change-step', 2);
        },
        emitSpaceName(name){
            this.$emit('send-space-name', name)
            this.continueStep()
        }
    }
}
</script>
