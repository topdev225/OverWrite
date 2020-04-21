import Vue from 'vue'
import Vuex from 'vuex'
import orders from './orders'
import notification from './notification'
import user from './user'
import campaign from './campaign'
import reports from './reports'
import { jsonapiModule } from 'jsonapi-vuex'
import axiosInstance from '../axios'

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    token: localStorage.getItem('user') ? 'Bearer' + ' ' + localStorage.getItem('user').replace(/['"]+/g, '') : null,
    account: null,
    title: ''
  },

  modules: {
    orders,
    notification,
    user,
    campaign,
    reports,
    jv: jsonapiModule(axiosInstance),
  },

  getters: {
    isSuperAdmin: state => {
      return state.account && state.account.role.name === 'Super Admin';
    },

    isShopper: state => {
      return state.account && state.account.role.name === 'Shopper';
    },

    isLoggedIn: state => {
      return state.account ? true : false;
    }
  },

  mutations: {
    setAccount(state, account) {
      state.account = account;
    }
  },

  actions: {
    async login({commit}, account) {
      localStorage.setItem('campaignId', account.campaign_id);
      localStorage.setItem('distributorId', account.distributor_id);
      localStorage.setItem('roleId', account.role_id);
      localStorage.setItem('roleName', account.role.name);

      commit('setAccount', account);
    },

    async logout({commit}) {
      localStorage.removeItem('campaignId');
      localStorage.removeItem('companyEmail');
      localStorage.removeItem('distributorId');
      localStorage.removeItem('firstName');
      localStorage.removeItem('lastName');
      localStorage.removeItem('roleId');
      localStorage.removeItem('roleName');
      localStorage.removeItem('selectedDepartment');
      localStorage.removeItem('selectedManager');
      localStorage.removeItem('selectedLocation');
      localStorage.removeItem('token');
      localStorage.removeItem('userId');

      commit('setAccount', null);
    }
  }
});