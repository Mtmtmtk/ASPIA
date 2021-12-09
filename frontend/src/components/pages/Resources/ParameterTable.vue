<template>
    <v-card
        class='grey darken-3'
    >
        <v-card-text>
            <v-data-table
                class='grey darken-3'
                :headers='headers'
                :items='tableItems'
                disable-sort
                hide-default-footer
            />
        </v-card-text>
    </v-card>
</template>
<script>
export default{
    data: () => ({
        headers:[
            { text: 'Acoustic Parameter', value: 'param' },
            { text: '31.25 Hz', value: '31' },
            { text: '62.5 Hz', value: '62' },
            { text: '125 Hz', value: '125' },
            { text: '250 Hz', value: '250' },
            { text: '500 Hz', value: '500' },
            { text: '1 kHz', value: '1k' },
            { text: '2 kHz', value: '2k' },
            { text: '4 kHz', value: '4k' },
            { text: '8 kHz', value: '8k' },
            { text: '16 kHz', value: '16k' },
        ],
    }),
    props:['tableItems']
}
</script>
