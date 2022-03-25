<template>
    <v-menu
        :close-on-content-click="false"
        offset-y
    >
        <template v-slot:activator="{ on, attrs }">
            <v-btn
                v-bind="attrs"
                v-on="on"
                fab
                x-small
                elevation="0"
            ><v-icon>mdi-dots-vertical</v-icon>
            </v-btn>
        </template>
        <v-list flat>
            <v-list-item
                v-for="item, i in items"
                :key="`config_${i}`"
                dense
            >
                <v-list-item-icon>
                    <v-icon>{{ item.icon }}</v-icon>
                </v-list-item-icon>
                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
    </v-menu>
</template>
<script>
export default{
    data:() => ({
        items:[
            { title:'Playback Speed', icon:'mdi-play-speed' }, 
            { title:'Download', icon:'mdi-download' }
        ]
    }) 
}
</script>
