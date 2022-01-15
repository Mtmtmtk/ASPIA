<template>
    <div>
        <v-row>
            <v-col class='text-body-1'>
                Audio Player
            </v-col>
        </v-row>
        <vue-plyr>
            <audio 
                controls 
                crossorigin
                playsinline
                :style='playerStyle'
            >
                <source
                    :src='audioURL'
                    type="audio/wav"
                />
            </audio>
        </vue-plyr>
    </div>
</template>
<script>
export default{
    data:() => ({
        playerStyle:{
            '--plyr-color-main':'#26A69A',
            '--plyr-audio-controls-background':'#E0E0E0',
        },
    }),
    props:['audioURL'],
    watch:{
        audioURL(){
            console.log(this.audioURL)
            document.querySelector('audio').load();
        }
    }
}
</script>
