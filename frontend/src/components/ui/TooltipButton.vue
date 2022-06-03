<template>
    <v-tooltip 
        v-bind="tooltipProps"
    >
        <template #activator="{ on, attrs }">
            <v-btn
                v-on="on"
                v-bind="{ ...attrs, ...defaultButtonProps, ...buttonProps }"
                :class="buttonClass"
                @click="onClick"
            ><v-icon v-html="buttonIcon"/>
            </v-btn>
        </template>
        <span v-html="tooltipHtmlText"/>
    </v-tooltip>
</template>
<script>
export default{
    data: () => ({
        defaultButtonProps: {
            xSmall: true,
            dark: true,
            fab: true,
            color: '#757575',
            elevation: '1'
        },
    }),
    props: {
        tooltipProps: {
            type: Object,
            default: () => ({})
        },
        tooltipHtmlText: {
            type: String,
            default: ''
        },
        buttonProps: {
            type: Object,
            default: () => ({})
        },
        buttonClass: {
            type: String,
            default: ''
        },
        buttonIcon: {
            type: String,
            default: ''
        }
    },
    methods: {
        onClick() {
            this.$emit('click');
        }
    },
}
</script>
