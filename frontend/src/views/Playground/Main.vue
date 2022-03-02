<template>
    <div>
        test
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
        console.log(this.duct)
        this.duct.invokeOnOpen(async () => {
            let ret = await this.duct.call(this.duct.EVENT.TEST,{
                test_running: "test"
            });
            console.log(ret);
        });
    }
}
</script>
