<template>
    <div>
        <slot name="left-icons-prepend" />

        <v-btn
            v-if="displayFlags.skipBackward"
            icon
            small
            @click="skipBackward"
        ><v-icon color="#616161">mdi-skip-backward</v-icon>
        </v-btn>

        <v-btn
            v-if="displayFlags.rewind"
            icon
            small
            @mousedown="startRewindingAudio"
            @mouseup="stopRewindingAudio"
        ><v-icon color="#616161">mdi-rewind</v-icon>
        </v-btn>


        <v-btn
            v-if="displayFlags.play"
            icon
            small
            @click="playPauseAudio"
        ><v-icon color="#616161">{{ icon }}</v-icon>
        </v-btn>

        <v-btn
            v-if="displayFlags.fastForward"
            icon
            small
            @mousedown="startFastForwardingAudio"
            @mouseup="stopFastForwardingAudio"
        ><v-icon color="#616161">mdi-fast-forward</v-icon>
        </v-btn>

        <v-btn
            v-if="displayFlags.skipForward"
            icon
            small
            @click="skipForward"
        ><v-icon color="#616161">mdi-skip-forward</v-icon>
        </v-btn>

        <slot name="left-icons-append"/>
    </div>
</template>
<script>
export default{
    data: () => ({
        icon: 'mdi-play', 
        counter: 0
    }), 
    props: ['displayFlags', 'duration', 'currentTime', 'isPlaying'], 
    watch: {
        currentTime(){
            if((this.currentTime == this.duration) && this.isPlaying)this.playPauseAudio();
        }
    }, 
    methods: {
        playPauseAudio(){
            this.counter++;
            if(this.counter % 2 == 0){
                this.icon = 'mdi-play';
                this.$emit('pause');
            }else{
                this.icon = 'mdi-pause'
                this.$emit('play');
            }
        }, 
        skipBackward(){
            this.$emit('skip-backward');
        }, 
        startRewindingAudio(){
            this.$emit('start-rewind');
        }, 
        stopRewindingAudio(){
            this.$emit('stop-rewind');
        }, 
        startFastForwardingAudio(){
            this.$emit('start-fast-forward');
        }, 
        stopFastForwardingAudio(){
            this.$emit('stop-fast-forward');
        }, 
        skipForward(){
            this.$emit('skip-forward');
        }, 
    }
}
</script>
