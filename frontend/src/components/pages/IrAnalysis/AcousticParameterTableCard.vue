<template>
    <v-card 
        rounded="lg"
        elevation="5"
        dark
    >
        <loading-overlay :loading="loading"/>
        <v-card-title>Acoustic Parameters Table</v-card-title>
        <v-card-text>
            Hover over the acoustic paramter columns to see the definition and meaning of each parameter.
            <acoustic-parameter-table :items="items"/>
        </v-card-text>
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import AcousticParameterTable from '@/components/ui/AcousticParameterTable'
export default{
    components:{
        LoadingOverlay,
        AcousticParameterTable
    },
    data:() => ({
        items:[],
    }),
    props:['acousticParameters','loading'],
    methods:{
        renderTable(){
            if(this.acousticParameters.length != 0){
                this.items = [ ...this.acousticParameters ]; 
                this.items[0].parameter = 'RT60 (s)'
                this.items[1].parameter = 'EDT (s)'
                this.items[3].parameter = 'C50 (dB)'
                this.items[4].parameter = 'C80 (dB)'
                this.items[5].parameter = 'Ts (s)'
            }
        }
    },
    watch:{
        acousticParameters(){
            this.renderTable();
        },
    },
}
</script>
