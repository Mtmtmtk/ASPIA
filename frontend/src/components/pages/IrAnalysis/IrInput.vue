<template>
    <v-card 
        rounded='lg'
        elevation='5' 
        dark 
        color='#323232'
    >
        <v-row class='ps-5 pt-3'>
            <v-col>
                Choose an impulse response vue you want to analyse.
            </v-col>
        </v-row>
        <v-card-text>
            <v-file-input
                label='Choose IR'
                prepend-icon='mdi-paperclip'
                @change='getIRData'
            >
            </v-file-input>
        </v-card-text>

        <v-row v-if='manualSplRateInput' class='ps-5 pt-3'>
            <v-col>
                Coundn't get a sampling rate from the file. Please enter it manually.
            </v-col>
        </v-row>
        <v-card-text v-if='manualSplRateInput'>
            <v-col cols='4'>
                <v-text-field
                    v-model='manualSplRate'
                    @blur='changeSplRate'
                    suffix='Hz'
                />
            </v-col>
        </v-card-text>

        <v-row v-if='manualChannelsInput' class='ps-5 pt-3'>
            <v-col>
                Coundn't get a number of channels from the file. Please enter it manually.
            </v-col>
        </v-row>
        <v-card-text v-if='manualChannelsInput'>
            <v-col cols='4'>
                <v-text-field
                    v-model='manualChannels'
                    @blur='changeChannels'
                />
            </v-col>
        </v-card-text>

        <v-card-text>
            <v-row>
                <v-col>
                    <v-btn
                        color='#26A69A'
                        :disabled='buttonDisbled'
                        @click='startAnalysis'
                    >
                        start analysis
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
export default{
    data:() => ({
        recording:[],
        recordingSplRate:null,
        channels:null,
        manualSplRateInput:false,
        manualChannelsInput:false,
        manualSplRate:0,
        manualChannels:0,
    }),
    computed:{
        buttonDisbled(){
            if(this.recording.length != 0  && (![this.recordingSplRate,this.channels].includes(0))) return false
            else return true
        }
    },
    methods:{
        getIRData(file){
            if(file){
                const reader = new FileReader();
                const vue = this;
                reader.onloadend = function(evt) {
                    vue.recording = Array.from(new Int16Array(evt.target.result));

                    const view = new DataView(evt.target.result);
                    vue.recordingSplRate = view.getUint32(24, true);
                    if(vue.recordingSplRate == 0) vue.manualSplRateInput = true;
                    else vue.manualSplRateInput = false;

                    vue.channels=view.getUint16(22,true);
                    if(vue.channels == 0) vue.manualChannelsInput = true;
                    else vue.manualChannelsInput = false;
                    
                };
                reader.readAsArrayBuffer(file);
            }else{
                this.recording = [];
                this.recordingSplRate = null;
                this.channels = null;
                this.manualChannelsInput = false;
                this.manualSplRateInput = false;
            }
        },
        changeSplRate(){
            this.recordingSplRate = parseInt(this.manualSplRate);
        },
        changeChannels(){
            this.channels = parseInt(this.manualChannels);
        },
        startAnalysis(){
            this.$emit('change-component', 'ir-analysis');
            this.$emit('get-ir-info', [ this.recording, this.recordingSplRate, this.channels ]);
        }
    }

}
</script>
