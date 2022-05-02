<template>
    <v-card color="#E0E0E0">
        <v-card-title>Spectrogram ({{ mode[0].toUpperCase() + mode.substring(1) }}) Setting</v-card-title>
        <v-card-text>
            <v-row>
                <v-col cols="12" class="pb-0">
                    <v-text-field 
                        outlined
                        dense
                        :value="maxVal"
                        type="number"
                        step="0.01"
                        color="#26A69A"
                        :label="labels[0]"
                        @change="emitValueChange('maxVal', $event)"
                    />
                </v-col>
                <v-col cols="12" class="py-0">
                    <v-text-field 
                        outlined
                        dense
                        :value="minVal"
                        type="number"
                        step="0.01"
                        color="#26A69A"
                        :label="labels[1]"
                        @change="emitValueChange('minVal', $event)"
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
            <v-spacer></v-spacer>
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
        ]
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
        },
    },
    computed: {
        labels() {
            if(this.mode == 'decibel')
                return ['Max Decibel', 'Min Decibel']
            else if(this.mode == 'power')
                return ['Max Power', 'Min Power']
            else(this.mode == 'amplitude')
                return ['Max Amplitude', 'Min Amplitude']
        }
    },
    methods: {
        onClickCancel(){
            this.$emit('close-dialog');
        },
        onClickConfirm(){
            this.$emit('confirm-changes');
        },
        emitValueChange(name, val){
            const updateEvent = `update:${name}`;
            let updateVal = (name == 'colorScale') ? val : parseFloat(val);
            this.$emit(updateEvent, updateVal);
        }
    }
}
</script>
