<template>
    <v-card height='570' class='ma-0 pa-0 overflow-auto'>
        <v-card-title>Sound Convolution</v-card-title>
        <v-card-text class='text-body-1'>
            <v-row>
                <v-col>
                    {{sentences[0]}}
                </v-col>
            </v-row>
        </v-card-text>
    </v-card>
</template>
<script>
//import { VueMathjax } from 'vue-mathjax'
export default{
    //components:{ VueMathjax },
    data:() => ({
        sentences:[
            'test'
        ],
        formulas:[
        ],
    }),
}
</script>
