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
import StepChanger from '../../ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        library,
        selectedChannels:'',
        outputChannelItems:[],
    }),
    props:['IrAudioType'],
    methods:{
        changeStep(val){
            this.$emit('change-step',val);
            if(val == 1) this.$emit('emit-output-channels', this.selectedChannels);
        }
    },
    watch:{
        IrAudioType(){
            console.log(this.IrAudioType);
            if(this.IrAudioType == 'stereo'){
                this.outputChannelItems = ['stereo', 'mono'];
            }else if(this.IrAudioType == 'mono'){
                this.outputChannelItems = ['mono'];
            }else if(this.IrAudioType == 'b-format'){
                this.outputChannelItems = ['b-format', 'stereo', 'mono'];
            }
        }
    } 
}
</script>
