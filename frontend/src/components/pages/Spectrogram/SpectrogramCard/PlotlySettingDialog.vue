<template>
    <v-row class="py-0 pr-4 my-0">
        <v-col cols="12" class="pb-0 pr-9 d-flex justify-end">
            <v-dialog
                v-model="dialog"
                width="500"
            >
                <template #activator="{ on, attrs }">
                    <v-btn
                        v-on="on"
                        v-bind="attrs"
                        color="#26A69A"
                        small
                        dark  
                        rounded
                    ><v-icon>mdi-cog</v-icon>
                    </v-btn>
                </template>
                <dialog-content
                    :mode="mode"
                    :max-val.sync="relayVars.maxVal"
                    :min-val.sync="relayVars.minVal"
                    :color-scale.sync="relayVars.colorScale" 
                    @close-dialog="closeDialog"
                    @confirm-changes="onConfirmChanges"
                />
            </v-dialog>
        </v-col>
    </v-row>
</template>
<script>
import DialogContent from './DialogContent'
export default {
    components: { DialogContent },
    data: () => ({
        dialog: false,
        relayVars: {
            maxVal: 0,
            minVal: 0,
            colorScale: 'Jet'
        }
    }),
    props: {
        mode: {
            type: String,
            default: 'decibel'
        },
        maxVal: {
            type: Number,
            default: 0
        },
        minVal: {
            type: Number,
            default: 0
        },
        colorScale: {
            type: String,
            default: 'Jet'
        }
    },
    watch: {
        maxVal() {
            this.relayVars.maxVal = this.maxVal;
        },
        minVal() {
            this.relayVars.minVal = this.minVal;
        },
        colorScale() {
            this.relayVars.colorScale = this.colorScale;
        }
    },
    methods: {
        closeDialog(){
            this.dialog = false;
        },
        onConfirmChanges(){
            this.$emit('confirm-changes', this.relayVars);
            this.closeDialog();
        }
    },
    mounted() {
        this.relayVars.maxVal = this.maxVal;
        this.relayVars.minVal = this.minVal;
        this.relayVars.colorScale = this.colorScale;
    }
}
</script>
