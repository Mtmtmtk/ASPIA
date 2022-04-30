<template>
    <v-container>
        <v-row>
            <v-col>
                All done! Please download your original spatial audio.
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color="#AFB42B"
                    :href="audioUrl"
                    download
                >
                    <v-icon>mdi-download</v-icon>download
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import { library } from '../library.js'
export default{
    data: () => ({
        library,
    }),
    props:['spaceName','audioUrl'],
    //}
}
</script>
