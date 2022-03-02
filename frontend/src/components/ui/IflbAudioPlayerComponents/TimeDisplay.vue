<template>
    <div :style="fontSize" class="pt-1 pr-1">
        {{currentTimeInFormat}}/{{durationInFormat}}
    </div>
</template>
<script>
const fontSize={
    'font-size':'12px'
}
export default{
    data:()=>({
        fontSize
    }),
    props:{
        currentTime: {
            type: Number,
            default: () => (0)
        },
        duration: {
            type: Number,
            default: () => (0)
        }
    },
    computed:{
        currentTimeInFormat(){
            const currentMin = Math.floor(this.currentTime/60);
            const currentSec = Math.floor(this.currentTime - currentMin*60);
            return ('00' + currentMin).slice(-2) + ':' + ('00' + currentSec).slice(-2);
        },
        durationInFormat(){
            const durationMin = Math.floor(this.duration/60);
            const durationSec = Math.floor(this.duration - durationMin*60);
            return ('00' + durationMin).slice(-2) + ':' + ('00' + durationSec).slice(-2);
        }
    }
}
</script>
