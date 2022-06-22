<template>
    <v-row :class="rowClass">
        <v-col v-if="!isHtml">{{ connectedSentences }}</v-col>
        <v-col v-if="isHtml" v-html="connectedSentences" />
    </v-row>
</template>
<script>
export default {
    props: {
        sentences: {
            type: [ Array, String ],
            default: () => ([])
        },
        rowClass: {
            type: String,
            default: ''
        },
        isHtml: {
            type: Boolean,
            default: false
        }
    },
    computed: {
        connectedSentences() {
            let cSentences = '';
            if(Array.isArray(this.sentences)){
                for (let sentence of this.sentences) {
                    const _idx = this.sentences.indexOf(sentence);
                    if (_idx == 0) cSentences = sentence;
                    else cSentences = cSentences + ' ' + sentence;
                }
            }else{
                cSentences = this.sentences;
            }
            return cSentences
        }
    }
}
</script>
