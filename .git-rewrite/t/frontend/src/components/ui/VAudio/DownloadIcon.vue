<template>
    <v-btn
        icon
        small
        :href="src"
        download="sample"
    >
        <v-icon
            color="#616161" 
        >mdi-download
        </v-icon>
    </v-btn>
</template>
<script>
export default{
    props: ['src']
}
</script>
