<template>
    <v-card
        class="grey darken-3"
    >
        <v-card-text>
            <v-data-table
                class="grey darken-3"
                :headers="headers"
                :items="tableItems"
                disable-sort
                hide-default-footer
            />
        </v-card-text>
    </v-card>
</template>
<script>
import { octaveBands } from '../library.js'
export default{
    data: () => ({
        octaveBands
    }),
    computed:{
        headers(){
            const _headers = Array.from(this.octaveBands);
            _headers.unshift({ text: 'Acoustic Parameter', value: 'param' });
            console.log(_headers)
            return _headers
        }
    },
    props:['tableItems']
}
</script>
