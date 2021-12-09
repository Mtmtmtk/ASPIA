<template>
    <v-container>
        <v-row>
            <v-col cols='4'>
                <v-img 
                    :src='spacePlanImg'
                />
            </v-col>
            <v-col cols='6'>
                <v-select
                    id='ir'
                    v-model='selectedIR'
                    filled
                    color='#26A69A'
                    :items='audioItems'
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
        sampleItems:['position1','position2','position3','position4'],
        selectedIR:'',
    }),
    props:['spaceName'],
    computed:{
        spacePlanImg(){
            const _nameList = this.library.map(el => el.name)
            const _ind = _nameList.indexOf(this.spaceName);
            const _planImgList = this.library.map(el => el.plan);
            let _planImgAdr = '';
            if(_ind == -1){
                _planImgAdr = require('@/assets/plan/noImage.jpeg');
            }else{
                if(_planImgList[_ind] != undefined) _planImgAdr = _planImgList[_ind];
                else _planImgAdr = require('@/assets/plan/noImage.jpeg');
            } 
            return _planImgAdr
        },
        audioItems(){
            if(this.spaceName != ''){
                const _nameList = this.library.map(el => el.name)
                const _ind = _nameList.indexOf(this.spaceName);
                const _IRLists = this.library.map(el => el.ir);
                const _IRList = _IRLists[_ind]
                //const _filenames = _IRList.map(el => el.match(/([^/]*)\./)[1]);    
                return _IRList
            }else return []
        }
    },
    methods:{
        continueStep(){
            this.$emit('change-step', 5);
            this.$emit('submit-form', 'submit')
        },
        cancelStep(){
            this.$emit('change-step', 3);
        },
    },
    watch:{
        spaceName(){
            console.log(this.spaceName)
            this.selectedIR = ''
        }
    },
}
</script>
