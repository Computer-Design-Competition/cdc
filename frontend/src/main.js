import Vue from 'vue'
import App from './App.vue'
import Element from 'element-ui'
import axios from 'axios'
import VueRouter from 'vue-router'
import "./plugins/element";
import index from "./pages/index.vue"
import detail from "./pages/detail.vue"
import Highcharts from 'highcharts/highstock';
import HighchartsMore from 'highcharts/highcharts-more';
import HighchartsDrilldown from 'highcharts/modules/drilldown';
import Highcharts3D from 'highcharts/highcharts-3d';
import Highmaps from 'highcharts/modules/map';

HighchartsMore(Highcharts)
HighchartsDrilldown(Highcharts);
Highcharts3D(Highcharts);
Highmaps(Highcharts);
import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import '../node_modules/echarts/map/js/world.js' // 引入世界地图
import '../node_modules/echarts/map/js/china.js'

//路由
const routes = [{
    path: '/index',
    name: "index",
    component: index
  },
  {
    path: '/detail',
    name: "detail",
    component: detail
  }
]
const router = new VueRouter({
  routes
})
Vue.use(VueRouter)
Vue.use(Element)
Vue.config.productionTip = false
Vue.prototype.$axios = axios;
axios.defaults.withCredentials = true;

new Vue({
  router,
  render: h => h(App),
}).$mount('#app')