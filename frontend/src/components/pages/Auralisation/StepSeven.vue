<template>
    <v-container class="pt-0">
        <v-row>
            <v-col>
                All done! Please download your original spatial audio.
            </v-col>
        </v-row>
        <v-row class="mt-2">
            <v-col>
                <v-audio 
                    :src="audioUrl" 
                    :display-flags="{
                        downloadIcon: false
                    }"
                />
            </v-col>
        </v-row>
        <v-row>
            <v-col>
                <v-btn
                    color="#AFB42B"
                    :href="audioUrl"
                    download
                ><v-icon>mdi-download</v-icon>download
                </v-btn>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import { library } from '../library.js'
import VAudio from '@/components/ui/VAudio'
export default{
    components: { VAudio },
    data: () => ({
        library,
    }),
    props:['spaceName','audioUrl'],
}
</script>
