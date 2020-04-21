// The Vue build version to load with the `import` command
// (runtime-only or standalone) has been set in webpack.base.conf with an alias.
import Vue from 'vue'
import App from '@/App'
import store from '@/store'
import router from '@/router'
import axiosInstance from '@/axios';
import Vuetify from 'vuetify'
import VueMoment from 'vue-moment'
import 'vuetify/dist/vuetify.min.css'
import VDateRange from 'vuetify-daterange-picker'
import 'vuetify-daterange-picker/dist/vuetify-daterange-picker.css'
import './style.css';
import CKEditor from '@ckeditor/ckeditor5-vue';

import * as Sentry from '@sentry/browser';
import * as Integrations from '@sentry/integrations';

Sentry.init({
  environment: process.env.SENTRY_ENVIRONMENT,
  dsn: `https://${process.env.SENTRY_KEY}`,
  integrations: [new Integrations.Vue({Vue, attachProps: true, logErrors: true})],
});

/* Show toast message on request error */
axiosInstance.interceptors.response.use((r) => r, function (error) {
  if (error.response) {
    if (error.response.status === 401) {
      store.dispatch('raiseError', error);

      // FIXME: put this back in when done with testing
      // store.dispatch('logout');
    } else if (error.response.status != 404) {
      store.dispatch('raiseError', error);
    }

    return Promise.reject(error);
  }

  store.dispatch('raiseError', error);

  return Promise.reject(error);
});

Vue.use(Vuetify, {
  theme: {
    primary: '#44C038',
  }
})

Vue.use(CKEditor)

Vue.use(VDateRange)
Vue.use(VueMoment)


Vue.config.productionTip = false

Vue.filter('capitalize', function (value) {
  if (!value) return ''
  value = value.toString()
  return value.charAt(0).toUpperCase() + value.slice(1)
})

Vue.prototype.$axios = axiosInstance;

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  store,
  components: { App },
  template: '<App/>'
})
