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
                    :val-range.sync="relayVars.valRange"
                    :time-range.sync="relayVars.timeRange"
                    :frequency-range.sync="relayVars.frequencyRange"
                    :color-scale.sync="relayVars.colorScale" 
                    :file-changed="fileChanged"
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
            valRange: [0, 0],
            timeRange: [0, 0],
            frequencyRange: [0, 22050],
            colorScale: 'Jet'
        }
    }),
    props: {
        mode: {
            type: String,
            default: 'decibel'
        },
        valRange: {
            type: Array,
            default: () => ([0, 0])
        },
        timeRange: {
            type: Array,
            default: () => ([0, 0])
        },
        frequencyRange: {
            type: Array,
            default: () => ([0, 22050])
        },
        colorScale: {
            type: String,
            default: 'Jet'
        },
        fileChanged: {
            type: Boolean,
            default: false
        }
    },
    watch: {
        valRange() {
            this.relayVars.valRange = this.valRange;
        },
        timeRange() {
            this.relayVars.timeRange = this.timeRange;
        },
        frequencyRange() {
            this.relayVars.frequencyRange = this.frequencyRange;
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
        this.relayVars.timeRange[1] = this.timeLength;
        this.relayVars.valRange = this.valRange;
        this.relayVars.colorScale = this.colorScale;
    }
}
</script>
