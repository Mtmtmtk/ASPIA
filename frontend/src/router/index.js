import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/main',
    },
    {
        path: '/main',
        component: () => import("@/views/Main"),
        redirect: 'main/convolution',
        children: [
            {
                path: 'convolution',
                component: () => import("@/components/pages/Convolution")
            },
            {
                path: 'ir-analysis',
                component: () => import("../components/pages/IrAnalysis")
            },
            {
                path: 'spectrogram',
                component: () => import("../components/pages/Spectrogram")
            },
            {
                path: 'resources',
                component: () => import("../components/pages/Resources")
            },
            {
                path: 'theory',
                component: () => import("../components/pages/Theory")
            },
            {
                path: 'about-this-app',
                component: () => import("../components/pages/AboutThisApp")
            },
            {
                path: 'pg',
                component: () => import("../views/Playground/Main.vue")
            }
        ]
    },
]
const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
