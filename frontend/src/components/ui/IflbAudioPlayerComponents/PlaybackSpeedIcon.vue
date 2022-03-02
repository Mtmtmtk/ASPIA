<template>
    <v-menu offset-y>
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                v-bind="attrs"
                v-on="on"
                icon
                small
                elevation="0"
            ><v-icon>mdi-play-speed</v-icon>
            </v-btn>
        </template>
        <v-list flat>
            <v-list-item-group
                v-model="selectedItem"
                color="#E53935"
            >
                <v-list-item
                    v-for="item, i in items"
                    :key="`playback_speed_${i}`"
                    dense
                    @click="changePlaybackSpeed(item.val)"
                >
                    <v-list-item-content :color="item.color">
                        <v-list-item-title>{{item.title}}</v-list-item-title>
                    </v-list-item-content>
                </v-list-item>
            </v-list-item-group>
        </v-list>
    </v-menu>
</template>
<script>
export default{
    data:() =>({
        selectedItem:3,
        items:[
            { title:'x2.0',  val:'2.0', color:'#FFFFFF' },
            { title:'x1.5',  val:'1.5', color:'#FFFFFF' },
            { title:'x1.25', val:'1.25',color:'#FFFFFF' },
            { title:'x1.0',  val:'1.0', color:'#FFFFFF' },
            { title:'x0.75', val:'0.75',color:'#FFFFFF' },
            { title:'x0.5',  val:'0.5', color:'#FFFFFF' },
        ]
    }),
    methods:{
        changePlaybackSpeed(val){
            this.$emit('change-playback-speed',Number(val));
        }
    },
}
</script>
