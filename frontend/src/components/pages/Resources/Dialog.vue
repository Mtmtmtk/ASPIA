<template>
    <v-card>
        <v-card-title>{{ name }}</v-card-title>
        <v-card-text>
            <v-row justify="center" class="pb-0">
                <v-col>
                    <v-carousel
                        hide-delimiters
                        cycle
                        interval="2000"
                    >
                        <v-carousel-item 
                            v-for="(image,i) in images"
                            :key="`image_no_${i}`"
                        >
                            <v-card>    
                                <v-img contain height="500" :src="image"/>
                            </v-card>
                        </v-carousel-item>
                    </v-carousel>
                </v-col>
            </v-row>
            <v-row>
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
                    <v-audio
                        :src="audioSrc"
                        :display-flags="{
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
                <!--<v-col cols="6">
                    <v-btn color="#37474F">
                        <v-icon>mdi-download</v-icon>download IR
                    </v-btn>
                </v-col>-->
                <v-col cols="12" class="d-flex justify-end">
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
import AcousticParameterTable from '@/components/ui/AcousticParameterTable'
import VAudio from '@/components/ui/VAudio'
export default{
    components:{
        AcousticParameterTable,
        VAudio
    },
    props: ['name', 'description', 'images', 'tableItems', 'ir'],
    computed:{
        audioSrc(){
            return (this.ir != undefined) ? this.ir[0] : 0
        }
    },
    methods:{
        closeDialog(){
            this.$emit('close-dialog', false);
        }
    },
}
</script>
