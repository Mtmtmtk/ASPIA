<template>
    <v-card color="#323232">
        <v-card-title>References</v-card-title>
        <v-card-text>
            <p
                v-for="(ref, idx) in references"
                :key="`reference_${idx}`"
                v-html="`[${ idx + 1 }] ${ref}`"
                class="my-0"
            >
            </p>
        </v-card-text>
    </v-card>
</template>
<script>
export default {
    data: () => ({
        references: [
            'M. R. Schroeder, “New method of measuring reverberation time,” <i>The Journal of the Acoustical Society of America</i>, vol. 57, p. 1187, Jun 1965.',
            'Leslie L. Dolle, <i>Environmental Acoustics</i>, New York, NY, USA: MsGraw-Hill Book Company, 1972.',
            'Nebvraska Acoustics Group, "Typical Values", concerthalls.org, http://www.concerthalls.org/?page_id=147 (Accessed Feb. 3, 2022)',
            'Mike Barron, "Interpretation of Early Decay Times in Concert Auditoria", <i>Acta Acustica united with Acustica</i>, vol.81, pp.320-331, July 1995. [Online]. Avaliable: https://www.researchgate.net/publication/233681112_Interpretation_of_Early_Decay_Times_in_Concert_Auditoria (Accessed: Feb. 1, 2022)',
            'Nebvraska Acoustics Group, "Clarity", concerthalls.org, http://www.concerthalls.org/?page_id=86 (Accessed Feb. 3, 2022)',
            'Marshall Long, "An acoustics measurement program for evaluating auditoriums based on the early/late sound energy ratio," <i>Journal of the Acoustical Society of America</i>, vol.96, pp.2251-2261, 1994.'
        ]
    })
}
</script>
