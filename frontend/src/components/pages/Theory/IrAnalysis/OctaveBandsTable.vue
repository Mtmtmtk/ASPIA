<template>
    <v-card flat class="mt-0">
        <v-card-text class="d-flex justify-center pb-0 font-weight-light">
            Table 1. Centre Frequencies and Octave Bands
        </v-card-text>
        <v-card-text class="pt-0">
            <v-data-table 
                dense  
                outlined  
                class="grey darken-3"
                :headers="octaveBandHeaders"
                :items="octaveBandItems"
                disable-sort
                hide-default-footer
            />
        </v-card-text>
    </v-card>
</template>
<script>
export default { 
    data: () => ({
        octaveBandHeaders:[
            { text: 'Centre Frequency (Hz)', value: 'nominal' },
            { text: 'Lower Band Limit (Hz)', value: 'min'     },
            { text: 'Upper Band Limit (Hz)', value: 'max'     },
        ],
        octaveBandItems:[
            { nominal: '31.5',  min: '22',    max: '44'    },
            { nominal: '63',    min: '44',    max: '88'    },
            { nominal: '125',   min: '88',    max: '177'   },
            { nominal: '250',   min: '177',   max: '355'   },
            { nominal: '500',   min: '355',   max: '710'   },
            { nominal: '1000',  min: '710',   max: '1420'  },
            { nominal: '2000',  min: '1420',  max: '2840'  },
            { nominal: '4000',  min: '2840',  max: '5680'  },
            { nominal: '8000',  min: '5680',  max: '11360' },
            { nominal: '16000', min: '11360', max: '22720' },
        ]
    })
}
</script>
