<template>
    <v-container>
        <v-row>
            <v-col cols="4">
                <v-dialog
                    v-model="dialog"
                    width="500"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-card
                            v-on="on"
                            v-bind="attrs"
                            @click="dialog = true"
                        >
                            <v-img :src="planImg"/>
                        </v-card>
                    </template>
                    <v-card>
                        <v-img :src="planImg"/>
                        <v-card-text>
                            <v-btn 
                                dark
                                color="#26A69A"
                                @click="dialog = false"
                            >Close
                            </v-btn>
                        </v-card-text>
                    </v-card>
                </v-dialog>
            </v-col>
            <v-col cols='6'>
                <v-select
                    v-model="format"
                    filled
                    offset-y
                    color="#26A69A"
                    :items="formatItems"
                    label="Select IR Audio Format"
                    prepend-inner-icon="mdi-speaker-wireless"
                />
                <v-select
                    v-if="formatSelected"
                    v-model="ir"
                    filled
                    offset-y
                    color="#26A69A"
                    :items="IRItems"
                    label="Select Impulse Response"
                    prepend-inner-icon="mdi-waveform"
                />
            </v-col>
        </v-row>
        <step-changer 
            :continue-required="true"
            :continue-disabled="continueDisabled"
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
        abbr:'',
        formatItems:[],
        IRItems:[],
        format:'',
        ir:'',
        dialog:false,
    }),
    props:[ 'spaceName', 'duct' ],
    computed: {
        planImg(){
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            const _planImgList = this.library.map(el => el.plan);
            const _planImgAdr = (_idx == -1 || _planImgList[_idx] == undefined) ? require('@/assets/plan/noImage.jpeg') : _planImgList[_idx];
            return _planImgAdr
        },
        formatSelected(){
            return (this.format != '') ? true : false
        },
        continueDisabled(){
            return (this.ir == '') ? true : false
        }
    },
    watch: {
        async spaceName(){
            this.initializeData();
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            this.abbr = this.library.map(el => el.abbr)[_idx];
            this.formatItems = await this.duct.call(this.duct.EVENT.AUDIO_TYPE_GET, { abbr: this.abbr })
        },
        async format(){
            this.ir = '';
            this.IRItems = await this.duct.call( this.duct.EVENT.IR_LIST_GET, { abbr: this.abbr, audioType: this.format });
        },
    },
    methods: {
        changeStep(val){
            this.$emit('change-step', val);
            if(val == 1) 
                this.$emit('get-ir-path', [ this.abbr, this.format, this.ir ]);
        },
        initializeData(){
            this.ir = '';
            this.format = '';
            this.formatItems = [];
            this.IRItems = [];
        }
    }
}
</script>
