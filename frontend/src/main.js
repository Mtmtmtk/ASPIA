import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify.js'
import VuePlyr from './plugins/vue-plyr.js'
import VueMathjax from './plugins/vue-mathjax.js'

Vue.config.productionTip = false

new Vue({
  router,  
  vuetify,
  VuePlyr,  
  VueMathjax,
  render: h => h(App),
}).$mount('#app')
