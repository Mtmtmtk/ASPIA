<template>
    <v-card light>
        <v-row>
            <v-col cols="12" class="d-flex justify-center py-1 px-5">
                <left-icons
                    :isRequired="leftIconsRequired"
                    :duration="duration"
                    :current-time="currentTime"
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
                        v-if="isRequiredEdited.seekBar"
                        :duration="duration"
                        :current-time="currentTime"
                        @seeked="changeCurrentTime"
                    />
                </slot>

                <slot name="time-display" :currentTime="currentTime" :duration="duration">
                    <time-display 
                        v-if="isRequiredEdited.timeDisplay"
                        :duration="duration"
                        :current-time="currentTime"
                    />
                </slot>

                <slot name="right-icons-prepend"
                    :volume="volume"
                    :audioSrc="src"
                    :methods="methods"
                />

                <volume-icon
                    v-if="isRequiredEdited.volumeIcon"
                    :volume.sync="volume"
                />
                <playback-speed-icon
                    v-if="isRequiredEdited.playbackSpeedIcon"
                    @change-playback-speed="changePlaybackSpeed"
                />
                <download-icon
                    v-if="isRequiredEdited.downloadIcon"
                    :src="src"
                />

                <slot name="right-icons-append" 
                    :volume="volume"
                    :audioSrc="src"
                    :methods="methods"
                />
            </v-col>
        </v-row>
    </v-card>
</template>
<script>
import LeftIcons from './IflbAudioPlayerComponents/LeftIcons'
import SeekBar from './IflbAudioPlayerComponents/SeekBar'
import TimeDisplay from './IflbAudioPlayerComponents/TimeDisplay'
import VolumeIcon from './IflbAudioPlayerComponents/VolumeIcon'
import PlaybackSpeedIcon from './IflbAudioPlayerComponents/PlaybackSpeedIcon'
import DownloadIcon from './IflbAudioPlayerComponents/DownloadIcon'

const defaultComponentsRequired={
    'play':true,
    'fastForward':true,
    'rewind':true,
    'skipForward':true,
    'skipBackward':true,
    'seekBar':true,
    'timeDisplay':true,
    'volumeIcon':true,
    'playbackSpeedIcon':true,
    'downloadIcon':true
}
export default{
    components:{
        LeftIcons,
        SeekBar,
        TimeDisplay,
        VolumeIcon,
        PlaybackSpeedIcon,
        DownloadIcon
    },
    data:() =>({
        defaultComponentsRequired,
        audio: new Audio(),
        volume:0.5,
        duration:0,
        currentTime:0,
        playIntvlFunc:null,
        rewindIntvlFunc:null,
        fastForwardIntvlFunc:null,
        leftIconsSlots:[
            'left-icons-prepend',
            'left-icons-append',
        ],
    }),
    props:{
        src: {
            type: String,
            default: () => ('')
        },
        isRequired: {
            type: Object,
            default: () => ({})
        }
    },
    watch:{
        src(){
            console.log(this.src)
            this.audio = new Audio(this.src);
            this.audio.volume = 0.5;
            this.volume=this.audio.volume;
            this.audio.addEventListener('loadedmetadata',() => {
                this.duration = this.audio.duration;        
            });
        },
        volume(){
            this.audio.volume=this.volume;
        },
    },  
    computed:{
        isRequiredEdited(){
            return {...this.defaultComponentsRequired, ...this.isRequired}
        },
        leftIconsRequired(){
            return {
                'play': this.isRequiredEdited.play,
                'fastForward': this.isRequiredEdited.fastForward,
                'rewind': this.isRequiredEdited.rewind,
                'skipForward': this.isRequiredEdited.skipForward,
                'skipBackward': this.isRequiredEdited.skipBackward,
            }
        },
        methods(){
            return {
                play: this.play,
                pause:this.pause, 
                rewindOnce:this.rewindOnce, 
                startRewind:this.startRewind, 
                stopRewind:this.stopRewind, 
                fastForwardOnce:this.fastForwardOnce, 
                startFastForward:this.startFastForward, 
                stopFastForward:this.stopFastForward, 
                skipBackward: this.skipBackward, 
                skipForward:this.skipForward,
                changePlaybackSpeed:this.changePlaybackSpeed,
                getCurrentTime:this.getCurrentTime
            }
        }  
    },
    methods:{
        play(){
            this.audio.play();
            this.playIntvlFunc = setInterval(()=>{
                this.currentTime = this.audio.currentTime;
            },100);
        },
        pause(){
            this.audio.pause();
            clearInterval(this.playIntvlFunc);
        },
        rewindOnce(val=10){
            this.audio.currentTime = this.audio.currentTime - val;
            this.currentTime = this.audio.currentTime;
        },
        startRewind(val=1,intvl=200){
            this.rewindIntvlFunc = setInterval(()=>{
                this.audio.currentTime = this.audio.currentTime - val;
                this.currentTime = this.audio.currentTime;
            },intvl);
        },
        stopRewind(){
            clearInterval(this.rewindIntvlFunc);
        },
        fastForwardOnce(val=10){
            this.audio.currentTime = this.audio.currentTime + val;
            this.currentTime = this.audio.currentTime;
        },
        startFastForward(val=1,intvl=200){
            this.fastForwardIntvlFunc = setInterval(()=>{
                this.audio.currentTime = this.audio.currentTime + val;
                this.currentTime = this.audio.currentTime;
            },intvl);
        },
        stopFastForward(){
            clearInterval(this.fastForwardIntvlFunc);
        },
        skipBackward(){
            this.audio.currentTime = 0;
            this.currentTime = this.audio.currentTime;
        },
        skipForward(){
            this.audio.currentTime = this.duration;
            this.currentTime = this.audio.currentTime;
        },
        changeCurrentTime(val){
            this.audio.currentTime = val;
            this.currentTime = this.audio.currentTime;
        },
        changePlaybackSpeed(val=1){
            this.audio.playbackRate = val;
        },
        getCurrentTime(){
            this.$emit('get-current-time', this.audio.currentTime);
        }
    },
    created(){
        this.audio = new Audio(this.src);
        this.audio.volume = 0.5;
        this.volume=this.audio.volume;
        this.audio.addEventListener('loadedmetadata',() => {
            this.duration = this.audio.duration;        
        });
    }
}
</script>
