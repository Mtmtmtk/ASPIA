<template>
    <v-expansion-panels
        focusable
    >
        <v-expansion-panel
            v-for='item in panelItems'
            :key='item.header'
        >
            <v-expansion-panel-header color='#323232'>
                {{item.header}}
            </v-expansion-panel-header>
            <v-expansion-panel-content color='#323232'>
                <component :is='item.component'/>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>
<script>
import ReverberationTime from './AcousticParameterCards/ReverberationTime'
import EarlyDecayTime from './AcousticParameterCards/EarlyDecayTime'
import CFifty from './AcousticParameterCards/CFifty'
import CEighty from './AcousticParameterCards/CEighty'
import DFifty from './AcousticParameterCards/DFifty'
export default{
    components:{
        ReverberationTime,
        EarlyDecayTime,
        CFifty,
        CEighty,
        DFifty
    },
    data:() => ({
        panelItems:[
            { header: 'Reverberation Time (RT60)', component:'reverberation-time'},
            { header: 'Early Decay Time (EDT)', component:'early-decay-time' },
            { header: 'C50', component:'c-fifty' },
            { header: 'C80', component:'c-eighty' },
            { header: 'D50', component:'d-fifty' },
        ]
    }),
    methods:{
        changeComponent(url){
            this.currentComponent = url;
            console.log(this.currentComponent)
        }
    }
}
</script>
