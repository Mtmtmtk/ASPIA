<template>
    <v-snackbar 
        v-model="snackbarModel"
        v-bind="{ ...snackbarAttrs }"
    >
        {{ snackbarText }}
        <template v-if="buttonRequired" #action="{ attrs }">
            <v-btn
                v-bind="attrs"
                color="red"
                text
                @click="closeSnackbar"
            >{{ buttonText }}
            </v-btn>
        </template>
    </v-snackbar>
</template>
<script>
export default {
    props: {
        snackbarModel: {
            type: Boolean
        },
        snackbarText: {
            type: String,
            default: ''
        },
        snackbarAttrs: {
            type: Object,
            default: () => ({})
        },
        buttonText: {
            type: String,
            default: ''
        },
        buttonRequired: {
            type: Boolean,
            default: true
        }
    },
    methods: {
        closeSnackbar(){
            this.$emit('update:snackbarModel', false);
        }
    }
}
</script>
