<template>
    <v-container>
        <v-row>
            <v-col cols="3" 
                v-for="hall in library" 
                :key="hall.name"
            >
                <v-card 
                    rounded="lg"
                    elevation="5"
                    @click="emitSpaceName(hall.name)"
                >
                    <v-img
                        :src=hall.images[0]
                        class="white--text"
                        :aspect-ratio="4/3"
                        gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
                    >
                        <v-responsive :aspect-ratio="4/3" class="align-end">
                            <v-card-text>{{ hall.name }}</v-card-text>
                        </v-responsive>
                    </v-img>
                </v-card>
            </v-col>
        </v-row>
        <step-changer 
            :continue-required="false"
            :cancel-required="true"
            :cancel-disabled="false"
            @change-step="changeStep"   
        />
    </v-container>
</template>
<script>
import { library } from '../library.js'
import StepChanger from '../../ui/StepChanger'
export default{
    components:{ StepChanger },
    data: () => ({
        library
    }),
    methods:{
        changeStep(val){
            this.$emit('change-step', val);
        },
        emitSpaceName(name){
            this.$emit('send-space-name', name)
            this.changeStep(1);
        }
    }
}
</script>
