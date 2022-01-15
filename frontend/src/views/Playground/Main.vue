<template>
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
