<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Spectrogram</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <audio-input
                    @get-audio-info="getAudioInfo"
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <spectrogram-result
                    v-if="resultShown" 
                    :duct="duct"
                    :src="src"
                    :analyser-node="analyserNode"
                    :resampled-audio="resampledAudioArray"
                    :channels="channels"
                    :timestamp="timestamp"
                    :duct-calling="ductCalling"
                />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import AudioInput from "./AudioInput"
import SpectrogramResult from "./SpectrogramResult"
export default{
    components:{ 
        AudioInput,
        SpectrogramResult, 
    },
    data:() => ({
        ductCalling:false,
        audioArray:[],
        audioSplRate:'',
        channels:'',
        src:'',
        fileName:'',
        resultShown:false,
        resampledAudioArray:[],
        timestamp:[]
    }),
    props:['duct'],
    watch:{
        audioArray(){
            if(this.audioArray.length != 0) this.callDuct();
        }
    },
    methods:{
        getAudioInfo(args){
            console.log(args);
            this.audioArray=args[0];
            this.audioSplRate=args[1];
            this.channels=args[2];
            this.src=args[3];
            this.fileName=args[4];
            this.analyserNode=args[5];
            this.resultShown=true;
        },
        async callDuct(){
            this.ductCalling = true;
            let resampledDict = {};
            [ resampledDict, this.timestamp ]  = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { arr: this.audioArray });
            this.resampledAudioArray = Object.values(resampledDict);
            console.log(this.resampledAudioArray);
            this.ductCalling = false;
        }
    }
}
</script>
