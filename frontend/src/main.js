import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify.js'
import VuePlyr from './plugins/vue-plyr.js'

Vue.config.productionTip = false

new Vue({
  router,  
  vuetify,
  VuePlyr,  
  render: h => h(App),
}).$mount('#app')
