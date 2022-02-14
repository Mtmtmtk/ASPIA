<template>
    <v-dialog
        v-model="dialog"
        width="750"
        dark
    >
        <template v-slot:activator="{ on, attrs }">
            <v-card 
                rounded="lg"
                v-bind="attrs"
                v-on="on"
                elevation="5"
            >
                <v-img
                    :src="image"
                    class="white--text"
                    :aspect-ratio="4/3"
                    gradient="to bottom, rgba(0,0,0,.1), rgba(0,0,0,.8)"
                >
                    <v-responsive :aspect-ratio="4/3" class="align-end">
                        <v-card-text>{{ name }}</v-card-text>
                    </v-responsive>
                </v-img>
            </v-card>
        </template>
        <card-dialog 
            :name="name"
            :description="description"
            :images="images"
            :table-items="tableItems"
            :ir="ir"
            @close-dialog="dialog = $event"
        />
    </v-dialog>
</template>
<script>
import CardDialog from './Dialog.vue'
export default{
    components:{
        CardDialog
    },
    data:() => ({
        dialog: false,
    }),
    props:['name','description','images','tableItems','ir'],
    computed:{
        image(){
            if(Array.isArray(this.images)) return this.images[0]
            else return this.images
        }
    }
}
</script>
