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
                    :duct="duct"
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
                    :file-name="fileName"
                    :resampled-audio="resampledAudioArray"
                    :channels="channels"
                    :timestamp="timestamp"
                    :sampling-points="samplingPoints"
                    :spect-db="spectDb"
                    :spect-pow="spectPow"
                    :spect-amp="spectAmp"
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
        timestamp:[],
        spectDb:[],
        spectPow:[],
        spectAmp:[],
        samplingPoints:2048
    }),
    props:['duct'],
    watch:{
        audioArray(){
            if(this.audioArray.length != 0) this.callDuct();
        }
    },
    methods:{
        getAudioInfo(args){
            this.audioArray=args[0];
            this.audioSplRate=args[1];
            this.channels=args[2];
            this.src=args[3];
            this.fileName=args[4];
            this.resultShown=true;
        },
        async callDuct(){
            this.ductCalling = true;
            let resampledDict = {};
            [ resampledDict, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: 'spectrogram' });
            this.resampledAudioArray = Object.values(resampledDict);

            this.spectDb = await this.duct.call(this.duct.EVENT.SPECTROGRAM_DB_GET,{
                spl_rate: this.audioSplRate,
                sampling_points: this.samplingPoints
            });
            this.spectPow = await this.duct.call(this.duct.EVENT.SPECTROGRAM_POWER_GET,{
                spl_rate: this.audioSplRate,
                sampling_points: this.samplingPoints
            });
            this.spectAmp = await this.duct.call(this.duct.EVENT.SPECTROGRAM_AMP_GET,{
                spl_rate: this.audioSplRate,
                sampling_points: this.samplingPoints
            });
            this.ductCalling = false;
        }
    },
    async beforeDestroy(){
        await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
    }
}
</script>
