<template>
    <v-row>
        <v-col>
            <v-btn
                v-if="continueRequired"
                :disabled="continueDisabled"
                color="#26A69A"
                @click="continueStep"
            >Continue
            </v-btn>
            <v-btn
                v-if="cancelRequired"
                text
                color="#8D6E63"
                @click="cancelStep"
            >Cancel
            </v-btn>
        </v-col>
    </v-row>
</template>
<script>
export default{
    props:['continueRequired','continueDisabled','cancelRequired'],
    methods:{
        continueStep(){
            this.$emit('change-step', 1);
        },
        cancelStep(){
            this.$emit('change-step', -1);
        },
    }
}
</script>
