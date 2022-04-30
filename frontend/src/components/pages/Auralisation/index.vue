<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Auralisation</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <stepper-view :duct="duct"/>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import StepperView from './StepperView.vue'
export default{
    components:{ StepperView },
    props:['duct'],
}
</script>
