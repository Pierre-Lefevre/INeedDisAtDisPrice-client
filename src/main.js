/* eslint-disable no-new */

import Vue from 'vue'
import App from './App'
import router from './router'
import store from '@/store/store'
import * as filters from '@/services/filters'

Object.keys(filters.default).forEach(key => {
  Vue.filter(key, filters.default[key])
})

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
