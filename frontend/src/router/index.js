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
        redirect: 'main/generator',
        children: [
            {
                path: 'generator',
                component: () => import("@/components/pages/Generator/index.vue")
            },
            {
                path: 'ir-analysis',
                component: () => import("../components/pages/IrAnalysis/index.vue")
            },
            {
                path: 'resources',
                component: () => import("../components/pages/Resources/index.vue")
            },
            {
                path: 'about-this-app',
                component: () => import("../components/pages/AboutThisApp/index.vue")
            }
        ]
    },
    {
        path: '/pg',
        component: () => import("@/views/Playground/Main"),
    },
]
const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
