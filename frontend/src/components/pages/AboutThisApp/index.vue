<template>
    <v-container>
        <v-row>
            <v-col class='text-h2'>
                <font color='#CFD8DC'>About this app</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols='12'>
                <contents-card/>
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import ContentsCard from './ContentsCard'
export default{
    components:{
        ContentsCard
    },
    data:() => ({
    }),
}
</script>
