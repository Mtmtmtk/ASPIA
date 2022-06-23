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
            'Peng R. D, "A very short course on time series analysis", https://bookdown.org/rdpeng/timeseriesbook/the-fast-fourier-transform-fft.html (Accessed: 2022-05-04).',
        ]
    })
}
</script>
