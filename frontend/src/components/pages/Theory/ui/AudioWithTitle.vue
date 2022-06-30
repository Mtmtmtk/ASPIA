<template>
    <v-card :color="backgroundColor" class="mt-0">
        <v-card-text class="pl-0 pt-2 font-weight-lighten">
            {{ title }}
        </v-card-text>
        <v-audio 
            :src="src"
            :display-flags="displyFlags"
        />
    </v-card>
</template>
<script>
import VAudio from '@/components/ui/VAudio'
export default {
    components: { 
        VAudio
    },
    props: {
        backgroundColor: {
            type: String,
            default: ''
        },
        title: {
            type: String,
            default: ''
        },
        src: {
            type: String,
            default: ''
        },
        displyFlags: {
            type: Object,
            default: () => ({})
        }
    }
}
</script>
