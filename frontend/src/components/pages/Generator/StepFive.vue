<template>
    <v-container>
        <v-row>
            <v-col>
                <v-select
                    v-model='selectedChannels'
                    filled
                    color='#26A69A'
                    :items='outputChannelItems'
                    label='Choose output channels'
                    prepend-inner-icon='mdi-speaker-multiple'
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
import { library } from '../library.js'
export default{
    data: () => ({
        library,
        selectedChannels:'',
        outputChannelItems:[],
    }),
    props:['IRAudioType'],
    methods:{
        continueStep(){
            this.$emit('change-step', 6);
            console.log('Five')
            this.$emit('call-ducts', this.selectedChannels);
        },
        cancelStep(){
            this.$emit('change-step', 4);
        }
    },
    watch:{
        IRAudioType(){
            console.log(this.IRAudioType);
            if(this.IRAudioType == 'stereo'){
                this.outputChannelItems = ['stereo', 'mono'];
            }else if(this.IRAudioType == 'mono'){
                this.outputChannelItems = ['mono'];
            }else if(this.IRAudioType == 'b-format'){
                this.outputChannelItems = ['b-format', 'stereo', 'mono'];
            }
        }
    } 
}
</script>
