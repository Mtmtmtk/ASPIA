<template>
    <v-card 
        rounded='lg'
        elevation='5' 
        dark
    >
        <v-overlay
            absolute
            color='#E0E0E0'
            :value='loading'
        >
            <v-progress-circular
                indeterminate
                color='#26A69A'
                size='64'
            />
        </v-overlay>
        <v-card-text>
            <v-data-table
                :headers='headers'
                :items='items'
            >
                <template v-slot:item.parameter='{ item }'>
                    <v-tooltip bottom>
                        <template v-slot:activator='{ on }'>
                            <span v-on='on'>{{ item.parameter }}</span>
                        </template>
                        <vue-mathjax :formula='sampleFormula' />
                    </v-tooltip>
                </template>
            </v-data-table>
        </v-card-text>
    </v-card>
</template>
<script>
import { VueMathjax } from 'vue-mathjax'
export default{
    components:{
        'vue-mathjax':VueMathjax
    },
    data:() => ({
        loading:true,
        headers:[
            { text: 'Acoustic Parameters', value:'parameter'},
            { text: '31.5 Hz', value:'31.5'},
            { text: '63 Hz', value:'63'},
            { text: '125 Hz', value:'125'},
            { text: '250 Hz', value:'250'},
            { text: '500 Hz', value:'500'},
            { text: '1 kHz', value:'1k'},
            { text: '2 kHz', value:'2k'},
            { text: '4 kHz', value:'4k'},
            { text: '8 kHz', value:'8k'},
            { text: '16 kHz', value:'16k'}
        ],
        formula:{
            'RT60 (s)': '',
            'EDT (s)':'',
            'D50':'',
            'C50 (dB)':'',
            'C80 (dB)':'',
        },
        items:[],
        sampleFormula:'$$x = {-b \\pm \\sqrt{b^2-4ac} \\over 2a}.$$'
    }),
    props:['acousticParameters'],
    watch:{
        acousticParameters(){
            if(this.acousticParameters.length != 0){
                this.items = this.acousticParameters; 
                console.log(this.items)
                this.items[0].parameter = 'RT60 (s)'
                this.items[1].parameter = 'EDT (s)'
                this.items[3].parameter = 'C50 (dB)'
                this.items[4].parameter = 'C80 (dB)'
                this.loading = false;
            }else{
                this.loading = true;
            }
        }
    },
    mounted(){
        if(this.acousticParameters.length != 0){
            this.items = this.acousticParameters; 
            console.log(this.items)
            this.items[0].parameter = 'RT60 (s)'
            this.items[1].parameter = 'EDT (s)'
            this.items[3].parameter = 'C50 (dB)'
            this.items[4].parameter = 'C80 (dB)'
            this.loading = false;
        }else{
            this.loading = true;
        }
    }
}
</script>
