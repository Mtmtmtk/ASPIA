<template>
    <v-card light>
        <v-overlay
            absolute
            :value="loading"
            z-index=2
            color="#FFFFFF"
            opacity="0.75"
        >
            <v-progress-circular
                indeterminate
                color='primary'
            />
        </v-overlay>
        <v-row>
            <v-col cols="12" class="d-flex justify-center py-1 px-5">
                <left-icons
                    :display-flags="leftIconsDisplayFlags"
                    :duration="duration"
                    :current-time="currentTime"
                    :is-playing="isPlaying"
                    @play="play"
                    @pause="pause"
                    @start-rewind="startRewind"
                    @stop-rewind="stopRewind"
                    @start-fast-forward="startFastForward"
                    @stop-fast-forward="stopFastForward"
                    @skip-backward="skipBackward"
                    @skip-forward="skipForward"
                >
                    <template v-for="slot in leftIconsSlots" #[`${slot}`]>
                        <slot 
                            :name="slot" 
                            :methods="{ 
                                play, 
                                pause, 
                                rewindOnce, 
                                startRewind, 
                                stopRewind, 
                                fastForwardOnce, 
                                startFastForward, 
                                stopFastForward, 
                                skipBackward, 
                                skipForward 
                            }"
                        />
                    </template>
                </left-icons>

                <slot name="seek-bar" :currentTime="currentTime" :duration="duration" :methods="{ changeCurrentTime }">
                    <seek-bar 
                        v-if="displayFlagsEdited.seekBar"
                        :duration="duration"
                        :current-time="currentTime"
                        @seeked="changeCurrentTime"
                        @change-mouse-condition="updateSeekBarManually"
                    />
                </slot>

                <slot name="time-display" :currentTime="currentTime" :duration="duration">
                    <time-display 
                        v-if="displayFlagsEdited.timeDisplay"
                        :duration="duration"
                        :current-time="currentTime"
                    />
                </slot>

                <slot name="right-icons-prepend"
                    :volume="volume"
                    :audioSrc="src"
                    :methods="allMethods"
                />

                <volume-icon
                    v-if="displayFlagsEdited.volumeIcon"
                    :volume.sync="volume"
                />
                <playback-speed-icon
                    v-if="displayFlagsEdited.playbackSpeedIcon"
                    @change-playback-speed="changePlaybackSpeed"
                />
                <download-icon
                    v-if="displayFlagsEdited.downloadIcon"
                    :src="src"
                />

                <slot name="right-icons-append" 
                    :volume="volume"
                    :audioSrc="src"
                    :methods="allMethods"
                />
            </v-col>
        </v-row>
    </v-card>
</template>
<script>
import LeftIcons from './LeftIcons'
import SeekBar from './SeekBar'
import TimeDisplay from './TimeDisplay'
import VolumeIcon from './VolumeIcon'
import PlaybackSpeedIcon from './PlaybackSpeedIcon'
import DownloadIcon from './DownloadIcon'

const defaultDisplayFlags = {
    play: true, 
    fastForward: true, 
    rewind: true, 
    skipForward: true, 
    skipBackward: true, 
    seekBar: true, 
    timeDisplay: true, 
    volumeIcon: true, 
    playbackSpeedIcon: true, 
    downloadIcon: true 
}
export default{
    components: {
        LeftIcons, 
        SeekBar, 
        TimeDisplay, 
        VolumeIcon, 
        PlaybackSpeedIcon, 
        DownloadIcon 
    }, 
    data: () => ({
        defaultDisplayFlags, 
        loading: true,
        audio: new Audio(), 
        volume: 0.5, 
        duration: 0, 
        currentTime: 0, 
        playIntvlFunc: null, 
        rewindIntvlFunc: null, 
        fastForwardIntvlFunc: null, 
        leftIconsSlots: [
            'left-icons-prepend', 
            'left-icons-append', 
        ],
        isPlaying: false
    }), 
    props: {
        src: {
            type: String, 
            default: () => ('')
        }, 
        displayFlags: {
            type: Object, 
            default: () => ({})
        }
    }, 
    watch: {
        src(){
            this.audio = new Audio(this.src);
            this.audio.volume = 0.5;
            this.volume = this.audio.volume;
            this.audio.addEventListener('loadedmetadata', () => {
                this.duration = this.audio.duration;        
                this.loading = false;
            });
        }, 
        volume(){
            this.audio.volume = this.volume;
        }, 
    },  
    computed: {
        displayFlagsEdited(){
            return { ...this.defaultDisplayFlags, ...this.displayFlags }
        }, 
        leftIconsDisplayFlags(){
            return {
                play: this.displayFlagsEdited.play, 
                fastForward: this.displayFlagsEdited.fastForward, 
                rewind: this.displayFlagsEdited.rewind, 
                skipForward: this.displayFlagsEdited.skipForward, 
                skipBackward: this.displayFlagsEdited.skipBackward, 
            }
        }, 
        allMethods(){
            return {
                play: this.play, 
                pause: this.pause, 
                rewindOnce: this.rewindOnce, 
                startRewind: this.startRewind, 
                stopRewind: this.stopRewind, 
                fastForwardOnce: this.fastForwardOnce, 
                startFastForward: this.startFastForward, 
                stopFastForward: this.stopFastForward, 
                skipBackward: this.skipBackward, 
                skipForward: this.skipForward, 
                changePlaybackSpeed: this.changePlaybackSpeed, 
                getCurrentTime: this.getCurrentTime
            }
        }  
    }, 
    methods: {
        play(){
            this.audio.play();
            this.isPlaying = true;
            this.playIntvlFunc = setInterval(() => {
                this.currentTime = this.audio.currentTime;
                this.emitCurrentTime();
            }, 100);
        }, 
        pause(){
            this.audio.pause();
            this.isPlaying = false;
            clearInterval(this.playIntvlFunc);
        }, 
        rewindOnce(val = 10){
            this.audio.currentTime = this.audio.currentTime - val;
            this.currentTime = this.audio.currentTime;
            this.emitCurrentTime();
        }, 
        startRewind(val = 1, intvl = 200){
            this.rewindIntvlFunc = setInterval(() => {
                this.audio.currentTime = this.audio.currentTime - val;
                this.currentTime = this.audio.currentTime;
                this.emitCurrentTime()
            }, intvl);
        }, 
        stopRewind(){
            clearInterval(this.rewindIntvlFunc);
        }, 
        fastForwardOnce(val = 10){
            this.audio.currentTime = this.audio.currentTime + val;
            this.currentTime = this.audio.currentTime;
            this.emitCurrentTime();
        }, 
        startFastForward(val = 1, intvl = 200){
            this.fastForwardIntvlFunc = setInterval(() => {
                this.audio.currentTime = this.audio.currentTime + val;
                this.currentTime = this.audio.currentTime;
                this.emitCurrentTime();
            }, intvl);
        }, 
        stopFastForward(){
            clearInterval(this.fastForwardIntvlFunc);
        }, 
        skipBackward(){
            this.audio.currentTime = 0;
            this.currentTime = this.audio.currentTime;
            this.emitCurrentTime();
        }, 
        skipForward(){
            this.audio.currentTime = this.duration;
            this.currentTime = this.audio.currentTime;
            this.emitCurrentTime();
        }, 
        changeCurrentTime(val){
            this.audio.currentTime = val;
            this.currentTime = this.audio.currentTime;
            this.emitCurrentTime();
        }, 
        changePlaybackSpeed(val = 1){
            this.audio.playbackRate = val;
        }, 
        emitCurrentTime(){
            this.$emit('emit-current-time', this.audio.currentTime);
        },
        updateSeekBarManually(type){
            if(this.isPlaying){
                if(type == 'mousedown') clearInterval(this.playIntvlFunc);
                else if(type == 'mouseup'){
                    this.playIntvlFunc = setInterval(() => {
                        this.currentTime = this.audio.currentTime;
                        this.emitCurrentTime();
                    }, 100);
                }
            }
        }
    }, 
    mounted(){
        this.audio = new Audio(this.src);
        this.audio.volume = 0.5;
        this.volume = this.audio.volume;
        this.audio.addEventListener('loadedmetadata', () => {
            this.duration = this.audio.duration;        
            this.loading = false;
        });
    }
}
</script>
