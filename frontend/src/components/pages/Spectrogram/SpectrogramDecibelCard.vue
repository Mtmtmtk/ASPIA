<template>
    <v-card
        light
        flat
        tile
        height="432"
        color="#E0E0E0"
    >
        <loading-overlay 
            :loading="loading"
        />
        <v-card-text class="pb-0">
            <v-row>
                <v-col cols="5" class="pb-0">
                    <v-text-field
                        v-model="absMinDB"
                        outlined
                        dense
                        label="Minimum decibel"
                        type="number"
                        prefix="-"
                    />    
                </v-col>
                <v-col cols="5" class="pb-0">
                    <v-text-field
                        v-model="absMaxDB"
                        outlined
                        dense
                        label="Maximum decibel"
                        type="number"
                        prefix="-"
                    />    
                </v-col>
                <v-col cols="2" class="pb-0">
                    <v-btn
                        color="#26A69A"
                        :sampling-points="samplingPoints"
                        dark
                        @click="applyRange"
                    >apply
                    </v-btn>
                </v-col>
            </v-row>
        </v-card-text>
        <spectrogram-canvas 
            :data="data"
            :mode="mode"
            :decibel-range="decibelRange"
            :sampling-points="samplingPoints"
            @emit-current-status="getCurrentStatus"
        />
    </v-card>
</template>
<script>
import LoadingOverlay from '@/components/ui/LoadingOverlay'
import SpectrogramCanvas from "@/components/ui/SpectrogramCanvas/index.vue"
export default{
    components:{ 
        SpectrogramCanvas,
        LoadingOverlay
    },
    data:()=>({
        loading:true,
        mode:'decibel',
        absMinDB:10,
        absMaxDB:0,
        decibelRange:[-10,0]
    }),
    props:{
        samplingPoints:{
            type: Number,
            default: () => (2048)
        },
        data:{
            type: Array,
            default: () => ([])
        },
    },
    methods:{
        applyRange(){
            this.decibelRange = [-1*this.absMinDB, -1*this.absMaxDB];
        },
        getCurrentStatus(val){
            if(val == 'drawing') this.loading = true;
            else if(val == 'finished') this.loading = false;
        }
    },
}
</script>

