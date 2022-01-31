<template>
    <div>
        <v-img
            :src='require("@/assets/img/openair.png")'
            contain
        >
        </v-img>
    </div>
</template>
<script>
import ducts from '@iflb/ducts-client'
export default{
    data:() => ({
        duct: new ducts.Duct(),
    }),
    methods:{
    },
    created(){
        this.duct.open("/ducts/wsd");

    }
}
</script>
