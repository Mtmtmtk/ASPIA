<template>
    <v-dialog
        v-model="dialog"
        width="500"
    >
        <template #activator="{ on }">
            <tooltip-button 
                v-on="{ on }"
                :tooltip-props="{ bottom: true }"
                tooltip-html-text="<span>Change styles</span>"
                button-icon="mdi-cog"
                @click="dialog = true"
            />
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
</template>
<script>
import DialogContent from './DialogContent'
import TooltipButton from '@/components/ui/TooltipButton'
export default {
    components: { 
        DialogContent,
        TooltipButton
    },
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
