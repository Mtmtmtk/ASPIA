<template>
    <v-container>
        <v-row>
            <v-col cols='4'>
                <v-dialog
                    v-model='dialog'
                    width='500' 
                >
                    <template v-slot:activator='{ on, attrs }'>
                        <v-card
                            v-on='on'
                            v-bind='attrs'
                            @click='dialog = true'
                        >
                            <v-img :src='spacePlanImg'/>
                        </v-card>
                    </template>
                    <v-card>
                        <v-img :src='spacePlanImg'/>
                        <v-card-text>
                            <v-btn 
                                color='#26A69A'
                                @click='dialog = false'
                            >Close
                            </v-btn>
                        </v-card-text>
                    </v-card>
                </v-dialog>
            </v-col>
            <v-col cols='6'>
                <v-select
                    v-model='selectedFormat'
                    filled
                    color='#26A69A'
                    :items='audioTypes'
                    label='Select IR Audio Format'
                    prepend-inner-icon='mdi-speaker-wireless'
                />
                <v-select
                    v-if='selectedFormat'
                    v-model='selectedIR'
                    filled
                    color='#26A69A'
                    :items='IRItems'
                    label='Select Impulse Response'
                    prepend-inner-icon='mdi-waveform'
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color='#26A69A'
                    :disabled='continueDisabled'
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
        audioTypes:[],
        IRItems:[],
        abbr:'',
        selectedFormat:'',
        selectedIR:'',
        dialog:false,
        continueDisabled:true
    }),
    props:['spaceName','duct'],
    computed:{
        spacePlanImg(){
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            const _planImgList = this.library.map(el => el.plan);
            let _planImgAdr = '';
            if(_idx == -1){
                _planImgAdr = require('@/assets/plan/noImage.jpeg');
            }else{
                if(_planImgList[_idx] != undefined) _planImgAdr = _planImgList[_idx];
                else _planImgAdr = require('@/assets/plan/noImage.jpeg');
            } 
            return _planImgAdr
        },
    },
    methods:{
        continueStep(){
            this.$emit('change-step', 5);
            this.$emit('send-abbr-audiotype-and-ir', [this.abbr,this.selectedFormat,this.selectedIR])
        },
        cancelStep(){
            this.$emit('change-step', 3);
        },
    },
    watch:{
        async spaceName(){
            console.log(this.spaceName);
            this.selectedIR = '';
            this.selectedFormat = '';
            this.audioTypes = [];
            this.IRItems = [];
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            this.abbr = this.library.map(el => el.abbr)[_idx];
            this.audioTypes = await this.duct.call(this.duct.EVENT.AUDIO_TYPE_GET, { abbr: this.abbr })
        },
        async selectedFormat(){
            this.selectedIR = '';
            this.IRItems = await this.duct.call(
                this.duct.EVENT.IR_LIST_GET, 
                { 
                    abbr: this.abbr, 
                    audioType: this.selectedFormat
                }
            );
        },
        selectedIR(){
            if(this.selectedIR != '') this.continueDisabled = false;
            else this.continueDisabled = true;
        }
    },
}
</script>
