<template>
    <v-container>
        <v-row>
            <v-col>
                <v-select
                    v-model="selectedChannels"
                    filled
                    color="#26A69A"
                    :items="outputChannelItems"
                    label="Choose output channels"
                    prepend-inner-icon="mdi-speaker-multiple"
                />
            </v-col>
        </v-row>
        <step-changer 
            :continue-required="true"
            :continue-disabled="false"
            :cancel-required="true"
            @change-step="changeStep"   
        />
    </v-container>
</template>
<script>
import { library } from '../library.js'
import StepChanger from '@/components/ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        library,
        selectedChannels:'',
        outputChannelItems:[],
    }),
    props:['irFormat'],
    methods:{
        changeStep(val){
            if(val == 1) 
                this.$emit('get-output-channels', this.selectedChannels);
            this.$emit('change-step',val);
        }
    },
    watch:{
        irFormat(){
            if(this.irFormat == 'b-format'){
                this.outputChannelItems = ['b-format', 'stereo', 'mono'];
            }else if(this.irFormat == 'stereo'){
                this.outputChannelItems = ['stereo', 'mono'];
            }else if(this.irFormat == 'mono'){
                this.outputChannelItems = ['mono'];
            }
        }
    } 
}
</script>
