<template>
    <v-slider 
        class="pl-1"
        :value="currentTime"
        hide-details
        color="#616161"
        track-color="#616161"
        step="0.001"
        min="0"
        :max="duration"
        @change="changeTime"
    />
</template>
<script>
export default{
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
    methods:{
        changeTime(val){
            this.$emit('seeked', val);
        }
    },
}
</script>
