<template>
    <v-container>
        <v-row>
            <v-col class="text-h2">
                <font color="#CFD8DC">Resources</font>
            </v-col>
        </v-row>
        <v-row>
            <v-col cols="3" 
                v-for="hall in library" 
                :key="hall.name"
            >
                <information-card 
                    :name="hall.name"
                    :description="hall.description"
                    :images="hall.images"
                    :table-items="hall.acousticParams"
                    :ir="hall.ir"
                />
            </v-col>
        </v-row>
    </v-container>
</template>
<script>
import InformationCard from './InformationCard'
import { library } from '../library.js'
export default{
    components:{ InformationCard },
    data:() => ({
        library
    }),
}
</script>
