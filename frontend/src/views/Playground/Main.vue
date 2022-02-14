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
import { test } from '../../components/pages/library.js'
export default{
    data:() => ({
        test,
        duct: new ducts.Duct(),
    }),
    created(){
        this.duct.open("/ducts/wsd");
        console.log(this.test);
    }
}
</script>
