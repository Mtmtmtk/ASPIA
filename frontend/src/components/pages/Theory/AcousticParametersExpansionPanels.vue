<template>
    <v-expansion-panels
        focusable
    >
        <v-expansion-panel
            v-for="item in panelItems"
            :key="item.header"
        >
            <v-expansion-panel-header color="#323232">
                {{item.header}}
            </v-expansion-panel-header>
            <v-expansion-panel-content color="#323232">
                <component :is="item.component"/>
            </v-expansion-panel-content>
        </v-expansion-panel>
    </v-expansion-panels>
</template>
<script>
import ReverberationTime from './AcousticParameterCards/ReverberationTime'
import EarlyDecayTime from './AcousticParameterCards/EarlyDecayTime'
import Clarity from './AcousticParameterCards/Clarity'
import Definition from './AcousticParameterCards/Definition'
export default{
    components:{
        ReverberationTime,
        EarlyDecayTime,
        Clarity,
        Definition
    },
    data:() => ({
        panelItems:[
            { header: 'Reverberation Time (RT60)', component:'reverberation-time'},
            { header: 'Early Decay Time (EDT)', component:'early-decay-time' },
            { header: 'Clarity (C50 and C80)', component:'clarity' },
            { header: 'Definition (D50)', component:'definition' },
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
