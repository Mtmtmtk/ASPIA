<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Spectrogram</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <font color="#CFD8DC">Spectrogram is an audio visualisation tool that can extract a sound strength at a certain frequency and time. Once you input a sound file and press 'Start Analysis' button, you can get three types of spectrogram; amplitude, power, power in decibel unit.</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <audio-input
                    :duct="duct"
                    :html-text="false"
                    key-type="spectrogram"
                    text="Choose an audio file whose spectrogram you want to look at."
                    @send-audio-info="getAudioInfo"
                    @emit-loading-error="showSnackbar"
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
                    @update-spectrogram="updateSpectrogram"
                />
            </v-col>
        </v-row>
        <error-snackbar
            :snackbar-attrs="{
                timeout: -1,
                color: 'grey darken-3',
                multiLine: true
            }"
            :snackbar-model.sync="errorSnackbar"    
            snackbar-text="Error occurred. Please reload the page. Please email the developer (ms2676@york.ac.uk) if you get this message repeatedly."
            button-text="close"
        />
    </v-container>
</template>
<script>
import AudioInput from "@/components/ui/AudioInput"
import SpectrogramResult from "./SpectrogramResult"
import ErrorSnackbar from "@/components/ui/Snackbar"
export default{
    components:{ 
        AudioInput,
        SpectrogramResult, 
        ErrorSnackbar
    },
    data:() => ({
        loading: false,
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
        samplingPoints:512,
        overlap: 50,
        windowVals: [],
        errorSnackbar: false,
        redisKey: '',
    }),
    props:['duct'],
    methods:{
        getAudioInfo(args){
            [ this.audioSplRate, this.channels, this.src, this.fileName, this.redisKey ] = args;
            this.callDuct();
            this.resultShown=true;
        },
        async callDuct(){
            this.loading = true;
            try {
                const startTime = performance.now();
                [ this.resampledAudio, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: this.redisKey });
                const resampleTime = performance.now();
                [ this.frequencies, this.timestamp, this.spectAmp, this.spectPow, this.spectDb ] = await this.duct.call(this.duct.EVENT.SPECTROGRAM_ALL_GET,{
                    group_key: this.redisKey,
                    spl_rate: this.audioSplRate,
                    sampling_points: this.samplingPoints,
                    window_type: this.windowType,
                    overlap_per: this.overlap
                });
                const spectrogramTime = performance.now();
                this.windowVals = await this.duct.call(this.duct.EVENT.WINDOW_GET, {
                    window_type: this.windowType,
                    sampling_points: this.samplingPoints
                });
                const windowTime = performance.now();
                this.loading = false;
                const endTime = performance.now();
                console.log(`resampling time: ${(resampleTime-startTime) / 1000 } seconds` );
                console.log(`spectrogram time: ${(spectrogramTime-resampleTime) / 1000 } seconds` );
                console.log(`window time: ${(windowTime-spectrogramTime) / 1000 } seconds` );
                console.log(`total time: ${(endTime-startTime) / 1000 } seconds` );
            }catch {
                this.showSnackbar();
            }
        },
        async calculateWindow(arr) {
            try {
                this.windowType = arr[0];
                this.samplingPoints = arr[1];
                this.windowVals = await this.duct.call(this.duct.EVENT.WINDOW_GET, {
                    window_type: this.windowType,
                    sampling_points: this.samplingPoints
                })
            }catch {
                this.showSnackbar();
            }
        },
        updateSpectrogram(arr) {
            [ this.windowType, this.samplingPoints, this.overlap ] = arr;
            this.callDuct();
        },
        showSnackbar(){
            this.errorSnackbar = true;
        }
    },
    mounted(){
        window.addEventListener('beforeunload', async () => {
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: this.redisKey });
            if(isKeyExists) await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: this.redisKey });
        });
    },
}
</script>
