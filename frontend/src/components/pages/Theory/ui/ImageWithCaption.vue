<template>
    <v-row class="d-flex justify-center my-0">
        <v-col     
            v-for="(image, idx) in images"
            :key="`image_${idx}`"
            :cols="colPerImage"
        >
            <v-card flat tile :color="color">
                <v-card-text class="d-flex justify-center py-0">
                    <v-img :width="imageWidth" :src="images[idx]" />
                </v-card-text>
                <v-card-text class="d-flex justify-center py-0">
                    <span class="font-weight-thin" style="color: #BDBDBD; font-size: 14px;"> Fig. {{ startIdx + idx  }}. {{ captions[idx] }}</span>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>
<script>
export default {
    props: {
        startIdx: {
            type: Number,
            default: 1
        },
        perRow: {
            type: Number,
            default: 1
        },
        color: {
            type: String,
            default: '#202020'
        },
        images: {
            type: Array,
            default: () => ([])
        },
        imageWidth: {
            type: String,
            default: '100%'
        },
        captions: {
            type: Array,
            default: () => ([])
        }
    },
    computed: {
        colPerImage() {
            return parseInt(12 / this.perRow)
        }
    }
}
</script>
