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
            ><v-icon>{{volumeIcon}}</v-icon>
            </v-btn>
        </template>
        <v-card>
            <v-slider 
                :value="volume"
                hide-details
                color="#616161"
                track-color="#616161"
                vertical
                step="0.01"
                min="0"
                max="1"
                @input="changeVolume"
            />
        </v-card>
    </v-menu>
</template>
<script>
export default{
    data:() =>({
        volumeIcon:'mdi-volume-high'
    }),
    props:['volume'],
    methods:{
        changeVolume(val){
            this.$emit('update:volume', val);
            if(this.volume == 0) this.volumeIcon='mdi-volume-off'
            else this.volumeIcon='mdi-volume-high'
        }
    }
}
</script>
