<template>
    <v-card>
        <v-card-title>{{ name }}</v-card-title>
        <v-card-text>
            <v-row justify='center'>
                <v-col cols='6'>
                    <v-img
                        contain
                        :src=image
                    />
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <strong>Description</strong>
                </v-col>
            </v-row>
            <v-row>
                <v-col class='text-justify'>{{ description }}</v-col>
            </v-row>
            <v-row>
                <v-col>
                    <strong>IR Example</strong>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <vue-plyr>
                        <audio 
                            controls 
                            crossorigin
                            playsinline
                            :style='playerStyle'
                        >
                            <source
                                :src=irExample
                                type="audio/wav"
                            />
                        </audio>
                    </vue-plyr>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <parameter-table :tableItems='tableItems'/>
                </v-col>
            </v-row>
            <v-row>
                <v-col cols='6'>
                    <v-btn color='#37474F'>
                        <v-icon>mdi-download</v-icon>download IR
                    </v-btn>
                </v-col>
                <v-spacer />
                <v-col cols='6' class='d-flex justify-end'>
                    <v-btn
                        color='#37474F'
                        @click='closeDialog'
                    >close
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
import ParameterTable from './ParameterTable.vue'

export default{
    components:{
        ParameterTable
    },
    data:() => ({
        playerStyle:{
            '--plyr-color-main':'#26A69A',
            '--plyr-audio-controls-background':'#E0E0E0',
            '--plyr-badge-border-radius':'100px',
        },
    }),
    props: ['name','description','image','tableItems','irExamples'],
    computed:{
        irExample(){
            if(this.irExamples != undefined) return this.irExamples[0]
            else return 0
        }
    },
    methods:{
        closeDialog(){
            this.$emit('close-dialog', false);
        }
    },
    created(){
        console.log(this.irExample);
    }

}
</script>
