<template>
    <v-container>
        <v-row>
            <v-col cols="4">
                <v-dialog
                    v-model="dialog"
                    width="80%"
                >
                    <template v-slot:activator="{ on, attrs }">
                        <v-carousel
                            v-on="on"
                            v-bind="attrs"
                            contiunuous
                            cycle
                            height="250"
                            :show-arrows="false"
                            interval="2000"
                        >
                            <v-overlay
                                absolute
                                light
                                opacity="0"
                                class="d-flex justify-end align-start"
                            >
                                <v-btn 
                                    icon
                                    @click="dialog = true"
                                ><v-icon color="#616161">mdi-arrow-expand-all</v-icon>
                                </v-btn>
                            </v-overlay>
                            <v-carousel-item 
                                v-for="(image,i) in planImgs"
                                :key="`image_no_${i}`"
                            ><v-card color="white"><v-img contain height="250" :src="image"/></v-card>
                            </v-carousel-item>
                        </v-carousel>
                    </template>
                    <v-card color="#424242" dark>
                        <v-card-title>
                            Plan
                            <v-spacer/>
                            <v-btn 
                                @click="dialog = false"
                                icon
                            ><v-icon>mdi-close</v-icon>
                            </v-btn>
                        </v-card-title>
                        <v-card-text>
                            <v-carousel
                                v-on="on"
                                v-bind="attrs"
                                height="700"
                            >
                                <v-carousel-item 
                                    v-for="(image,i) in planImgs"
                                    :key="`image_no_${i}`"
                                ><v-card color="white"><v-img contain height="650" :src="image"/></v-card>
                                </v-carousel-item>
                            </v-carousel>
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
        planImgs(){
            const _nameList = this.library.map(el => el.name);
            const _idx = _nameList.indexOf(this.spaceName);
            const _planImgsList = this.library.map(el => el.plan);
            const _planImgsAdr = (_idx == -1 || _planImgsList[_idx] == undefined) ? [ require('@/assets/plan/noImage.jpeg')] : _planImgsList[_idx];
            return _planImgsAdr
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
