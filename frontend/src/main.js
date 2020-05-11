import Vue from 'vue'
import App from './App.vue'
import myCharts from './plugins/echart.js'

Vue.use(myCharts)
Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')