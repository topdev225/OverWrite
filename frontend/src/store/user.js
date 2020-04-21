import axiosInstance from '../axios';

class User {
  constructor (data) {
    this.account_id = data.account_id;
    this.token = data.token;
    this.token_type = data.token_type
  }
}

export default {
  state: {
    user: null
  },
  mutations: {
    setUser (state, payload) {
      state.user = payload
    }
  },
  actions: {
    async loginUser ({commit}, {username, password}) {
      commit('clearError');
      commit('setLoading', true);
      try {
        const user = await axiosInstance.post(`/login`, {
          username: username,
          password: password
        });
        commit('setUser', new User(user.data));
      } catch (error) {
        commit('setError', error.message);
        throw error
      }
      commit('setLoading', false);
    },
  },
  getters: {
    user (state) {
      return state.user
    },
  }
}
