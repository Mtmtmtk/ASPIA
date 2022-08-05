<template>
    <v-tabs
        background-color="#E0E0E0"
        color="#26A69A"
        light
        v-model="inputValue"
        class="rounded-t-lg"
    >
        <v-tabs-slider />
        <v-tooltip top v-for="(el, idx) in tabHeaderInfo" :key="`tab_${idx}`">
            <template #activator="{ on }">
                <v-tab
                    v-on="on"
                >{{ el.title }}</v-tab>
            </template>
            <span v-html="el.tooltipHtml"/>
        </v-tooltip>
    </v-tabs>
</template>
<script>
export default {
    props: ['value', 'tabHeaderInfo'],
    computed: {
        inputValue: {
            get() {
                return this.value
            },
            set(newValue) {
                this.$emit('input', newValue)
            }
        }
    },
}
</script>
