<template>
    <v-menu
        :close-on-content-click="false"
        offset-y
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                small
                elevation="0"
            ><v-icon>{{ volumeIcon }}</v-icon>
            </v-btn>
        </template>
        <v-slider 
            class="overflow-hidden"
            :value="volume"
            hide-details
            color="#616161"
            track-color="#616161"
            background-color="#FFFFFF"
            vertical
            step="0.01"
            min="0"
            max="1"
            @input="changeVolume"
        />
    </v-menu>
</template>
<script>
export default{
    data: () => ({
    }), 
    props: ['volume'], 
    computed: {
        volumeIcon(){
            if(this.volume == 0) return 'mdi-volume-off'
            else return 'mdi-volume-high'
        }
    },
    methods: {
        changeVolume(val){
            this.$emit('update:volume', val);
        }
    },
}
</script>
