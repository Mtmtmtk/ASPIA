<template>
    <v-container>
        <v-row>
            <v-col class='text-h2'>
                <font color='#CFD8DC'>IR Analysis</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols='12'>
                <component
                    :is='currentComponent'
                    :duct='duct'
                    :irArr='irArr'
                    :splRate='splRate'
                    :channels='channels'
                    @change-component='changeComponent'
                    @get-ir-info='getIrInfo'
                />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import IrInput from './IrInput'
import IrAnalysis from './IrAnalysis'
export default{
    components:{
        IrInput,
        IrAnalysis
    },
    data:() =>({
        currentComponent:'ir-input',
        irArr:[],
        splRate:0,
        channels:0,
    }),
    props:['duct'],
    methods:{
        changeComponent(name){
            this.currentComponent = name;
        },
        getIrInfo(...args){
            args = args.flat();
            this.irArr    = args[0];
            this.splRate  = args[1];
            this.channels = args[2];
        }
    }
}
</script>
