<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Auralisation</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <font color="#CFD8DC">This function can add sound resonance to sounds recorded in an anechoic room as if they were originally recorded in a certain space. Only by going through the steps below, you can create an auralised sound file!</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="12">
                <stepper-view 
                    :duct="duct"
                    @notice-error="showSnackbar"
                />
            </v-col>
        </v-row>
        <error-snackbar
            :snackbar-attrs="{
                timeout: -1,
                color: 'grey darken-3',
                multiLine: true
            }"
            :snackbar-model.sync="errorSnackbar"    
            :snackbar-text="text"
            button-text="close"
        />
    </v-container>
</template>
<script>
import StepperView from './StepperView.vue'
import ErrorSnackbar from '../../ui/Snackbar'
export default{
    components:{ 
        StepperView,
        ErrorSnackbar
    },
    data: () => ({
        errorSnackbar: false,
        text: ''
    }),
    props:['duct'],
    methods: {
        showSnackbar(errorType) {
            this.text = `Error occurred. Please reload the page. Please email the developer (ms2676@york.ac.uk) with the error code if you get this message repeatedly. [error_code: ${errorType}]`;
            this.errorSnackbar = true;
        }
    }
}
</script>
