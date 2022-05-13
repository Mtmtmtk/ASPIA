<template>
    <v-card color="#E0E0E0">
        <v-card-title>Spectrogram ({{ mode[0].toUpperCase() + mode.substring(1) }}) Setting</v-card-title>
        <v-card-text>
            <v-row>
                <v-col cols="12" class="pb-0 pt-9">
                    <v-range-slider
                        :label="mode[0].toUpperCase() + mode.substring(1) + ' Range:'"
                        :min="accepectableValueRange[0]"
                        :max="accepectableValueRange[1]"
                        :value="valRange"
                        :step="step"
                        color="#26A69A"
                        thumb-color="#26A69A"
                        track-color="#EF5350"
                        thumb-label="always"
                        @change="emitValueChange('valRange', $event)"
                    />
                </v-col>
                <v-col cols="12" class="pb-0">
                    <v-range-slider
                        label="Time Range (s):"
                        :min="accepectableTimeRange[0]"
                        :max="accepectableTimeRange[1]"
                        :value="timeRange"
                        step="0.01"
                        color="#26A69A"
                        thumb-color="#26A69A"
                        track-color="#EF5350"
                        thumb-label="always"
                        @change="emitValueChange('timeRange', $event)"
                    />
                </v-col>
                <v-col cols="12" class="pb-0">
                    <v-range-slider
                        label="Frequency Range (Hz):"
                        :min="accepectableFrequencyRange[0]"
                        :max="accepectableFrequencyRange[1]"
                        :value="frequencyRange"
                        step="10"
                        color="#26A69A"
                        thumb-color="#26A69A"
                        track-color="#EF5350"
                        thumb-label="always"
                        @change="emitValueChange('frequencyRange', $event)"
                    />
                </v-col>
                <v-col cols="12" class="py-0">
                    <v-select
                        outlined
                        dense
                        offset-y
                        :value="colorScale"
                        color="#26A69A"
                        label="Color Scale"
                        :items="colorScales"
                        @change="emitValueChange('colorScale', $event)"
                    />
                </v-col>
            </v-row>
        </v-card-text>
        <v-card-actions>
            <v-spacer/>
            <v-btn
                color="error"
                text
                @click="onClickCancel"
            >Cancel
            </v-btn>
            <v-btn
                dark
                color="#26A69A"
                @click="onClickConfirm"
            >Confirm
            </v-btn>
        </v-card-actions>
    </v-card>
</template>
<script>
export default {
    data: () => ({
        colorScales: [
            'Jet',
            'Hot',
            'Greys',
            'Greens',
            'Electric',
            'Earth',
            'Bluered',
            'Blackbody',
            'Picnic',
            'Portland',
            'RdBu',
            'YlGnBu',
            'YlOrRd',
        ],
        accepectableFrequencyRange: [0, 22050],
        accepectableTimeRange: [0, 0]
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
    },
    computed: {
        accepectableValueRange() {
            if(this.mode == 'decibel') return [-50, 0]
            else return [0, 1]
        },
        step() {
            if(this.mode == 'decibel') return 1
            else return 0.01
        }
    },
    methods: {
        onClickCancel(){ this.$emit('close-dialog'); },
        onClickConfirm(){ this.$emit('confirm-changes'); },
        emitValueChange(name, val){
            const updateEvent = `update:${name}`;
            let updateVal = (name == 'colorScale') ? val : val.map(el => parseFloat(el));
            this.$emit(updateEvent, updateVal);
        }
    },
    created(){
        this.accepectableTimeRange = this.timeRange;
    }
}
</script>
