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
                    :loading="loading"
                    :src="src"
                    :file-name="fileName"
                    :resampled-audio="resampledAudio"
                    :channels="channels"
                    :frequencies="frequencies"
                    :timestamp="timestamp"
                    :spect-db="spectDb"
                    :spect-pow="spectPow"
                    :spect-amp="spectAmp"
                    :window-vals="windowVals"
                    @update-window-preview="calculateWindow"
                    @update-spectrogram="callDuct"
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
        loading: false,
        audioArray: [],
        audioSplRate: '',
        channels: '',
        src: '',
        fileName: '',
        resultShown: false,
        resampledAudio: [],
        timestamp: [],
        frequencies: [],
        spectDb: [],
        spectPow: [],
        spectAmp: [],
        windowType: 'Hamming',
        samplingPoints:2048,
        windowVals: []
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
            this.loading = true;
            let resampledDict = {};
            [ resampledDict, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: 'spectrogram' });
            this.resampledAudio = Object.values(resampledDict);
            [ this.frequencies, this.timestamp, this.spectAmp, this.spectPow, this.spectDb ] = await this.duct.call(this.duct.EVENT.SPECTROGRAM_ALL_GET,{
                spl_rate: this.audioSplRate,
                sampling_points: this.samplingPoints,
                window_type: this.windowType
            });
            this.windowVals = await this.duct.call(this.duct.EVENT.WINDOW_GET, {
                window_type: this.windowType,
                sampling_points: this.samplingPoints
            })
            this.loading = false;
        },
        async calculateWindow(arr) {
            this.windowType = arr[0];
            this.samplingPoints = arr[1];
            this.windowVals = await this.duct.call(this.duct.EVENT.WINDOW_GET, {
                window_type: this.windowType,
                sampling_points: this.samplingPoints
            })
        }
    },
    mounted(){
        window.addEventListener('beforeunload', async () => {
            await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
        });
    },
    async beforeDestroy(){
        await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
    }
}
</script>
