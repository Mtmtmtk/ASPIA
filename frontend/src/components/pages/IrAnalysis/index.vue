<template>
    <v-container>
        <v-row>
            <v-col class='text-h2'>
                <font color='#CFD8DC'>IR Analysis</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <ir-input
                    @get-ir-info='getIrInfo'
                />
            </v-col>
        </v-row>
        <v-row v-if='fileSelected'>
            <v-col>
                <ir-analysis
                    :duct='duct'
                    :irArr='irArr'
                    :splRate='splRate'
                    :channels='channels'
                    :audioURL='audioURL'
                    :fileName='fileName'
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
        irArr:[],
        splRate:0,
        channels:0,
        timestamp:[],
        audioURL:'',
        fileName:'',
        fileSelected: false
    }),
    props:['duct'],
    methods:{
        getIrInfo(...args){
            args = args.flat();
            this.irArr    = args[0];
            this.splRate  = args[1];
            this.channels = args[2];
            this.audioURL = args[3];
            this.fileName = args[4];
            this.fileSelected = false;
            this.$nextTick(()=> (this.fileSelected = true));
        },
    }
}
</script>