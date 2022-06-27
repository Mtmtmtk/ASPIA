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
                    :html-text="false"
                    group-key="spectrogram"
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
        errorSnackbar: false
    }),
    props:['duct'],
    methods:{
        getAudioInfo(args){
            [this.audioSplRate, this.channels, this.src, this.fileName] = args;
            this.callDuct();
            this.resultShown=true;
        },
        async callDuct(){
            this.loading = true;
            try {
                [ this.resampledAudio, this.timestamp ] = await this.duct.call(this.duct.EVENT.RESAMPLE_CHART_GET, { group_key: 'spectrogram' });
                [ this.frequencies, this.timestamp, this.spectAmp, this.spectPow, this.spectDb ] = await this.duct.call(this.duct.EVENT.SPECTROGRAM_ALL_GET,{
                    spl_rate: this.audioSplRate,
                    sampling_points: this.samplingPoints,
                    window_type: this.windowType,
                    overlap_per: this.overlap
                });
                this.windowVals = await this.duct.call(this.duct.EVENT.WINDOW_GET, {
                    window_type: this.windowType,
                    sampling_points: this.samplingPoints
                })
                this.loading = false;
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
            const isKeyExists = await this.duct.call(this.duct.EVENT.CHECK_GROUP_EXISTENCE, { group_key: 'spectrogram' });
            if(isKeyExists) await this.duct.call(this.duct.EVENT.DELETE_GROUP_IN_REDIS, { group_key: 'spectrogram' });
        });
    },
}
</script>
