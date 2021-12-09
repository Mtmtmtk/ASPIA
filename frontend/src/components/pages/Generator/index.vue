<template>
    <v-container>
        <v-row>
            <v-col class='text-h2'>
                <font color='#CFD8DC'>Generator</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols='12'>
                <stepper-view 
                    :duct='duct'
                />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import StepperView from './StepperView.vue'
import ducts from '@iflb/ducts-client'
export default{
    components:{
        StepperView
    },
    data:() => ({
        duct: new ducts.Duct(),
    }),
    created(){
        this.duct.open("/ducts/wsd");
    }
}
</script>
