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
                    v-model='selectedType'
                    filled
                    color='#26A69A'
                    :items='audioTypes'
                    label='Choose Audio Type'
                />
                <v-select
                    v-if='selectedType'
                    v-model='selectedIR'
                    filled
                    color='#26A69A'
                    :items='IRItems'
                    label='Choose Impulse Response'
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
        audioTypes:[],
        IRItems:[],
        abbr:'',
        selectedType:'',
        selectedIR:'',
        dialog:false
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
            this.$emit('send-type-and-ir', [this.selectedType,this.selectedIR])
        },
        cancelStep(){
            this.$emit('change-step', 3);
        },
    },
    watch:{
        async spaceName(){
            console.log(this.spaceName);
            this.selectedIR = '';
            this.selectedType = '';
            this.audioTypes = [];
            this.IRItems = [];
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            this.abbr = this.library.map(el => el.abbr)[_idx];
            this.audioTypes = await this.duct.call(this.duct.EVENT.AUDIO_TYPE_GET, { abbr: this.abbr })
        },
        async selectedType(){
            this.selectedIR = '';
            this.IRItems = await this.duct.call(
                this.duct.EVENT.IR_LIST_GET, 
                { 
                    abbr: this.abbr, 
                    audioType: this.selectedType
                }
            );
        }
    },
}
</script>
