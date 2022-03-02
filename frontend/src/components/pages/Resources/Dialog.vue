<template>
    <v-card>
        <v-card-title>{{ name }}</v-card-title>
        <v-card-text>
            <v-row justify="center" class="pb-0">
                <v-col>
                    <v-carousel
                        hide-delimiter-background
                        cycle
                        interval="2000"
                    >
                        <v-carousel-item 
                            v-for="(image,i) in images"
                            :key="`image_no_${i}`"
                        >
                            <v-card>    
                                <v-img contain :src="image"/>
                            </v-card>
                        </v-carousel-item>
                    </v-carousel>
                </v-col>
            </v-row>
            <v-row class="mt-0">
                <v-col>
                    <strong>Description</strong>
                </v-col>
            </v-row>
            <v-row>
                <v-col class="text-justify">{{ description }}</v-col>
            </v-row>
            <v-row>
                <v-col>
                    <strong>IR Example</strong>
                </v-col>
            </v-row>
            <v-row class="pb-2">
                <v-col>
                    <iflb-audio-player
                        :src="audioSrc"
                        :is-required="{
                            skipBackward:false,
                            skipForward:false,
                        }"
                    />
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <acoustic-parameter-table colorClass="grey darken-3" :items="tableItems"/>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols="6">
                    <v-btn color="#37474F">
                        <v-icon>mdi-download</v-icon>download IR
                    </v-btn>
                </v-col>
                <v-spacer />
                <v-col cols="6" class="d-flex justify-end">
                    <v-btn
                        color="#37474F"
                        @click="closeDialog"
                    >close
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import AcousticParameterTable from '../../ui/AcousticParameterTable'
import IflbAudioPlayer from '../../ui/IflbAudioPlayer'
export default{
    components:{
        AcousticParameterTable,
        IflbAudioPlayer
    },
    props: ['name','description','images','tableItems','ir'],
    computed:{
        audioSrc(){
            console.log(this.ir[0])
            if(this.ir != undefined) return this.ir[0]
            else return 0
        }
    },
    methods:{
        closeDialog(){
            this.$emit('close-dialog', false);
        }
    },
    created(){
    }
}
</script>
