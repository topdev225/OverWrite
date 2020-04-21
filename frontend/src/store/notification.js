export default {
  state: {
    message: null,
    color: 'success',
    show: false
  },
  mutations: {
    setMessage (state, payload) {
      state.message = payload;
    },
    setColor (state, payload) {
      state.color = payload;
    },
    toggle (state) {
      state.show = !state.show;
    },
  },
  actions: {
    raiseError({commit}, payload) {
      commit('setColor', 'error');

      if (typeof payload === 'string') {
        commit('setMessage', payload);
      } else if (payload instanceof Error) {
        let errorMsg = 'Unknown Error';

        if (payload.response && payload.response.data) {
          let data = payload.response.data;

          if (data.errors && data.errors[0].detail) {
            // this captures errors from SAFRS
            errorMsg = data.errors[0].detail;
          } else if (data.message) {
            // this captures errors from flask
            errorMsg = data.message;
          }
        }

        commit('setMessage', errorMsg);
      } else if (typeof payload == 'object') {
        commit('setMessage', payload.message);
      }

      commit('toggle')
      setTimeout(() => {commit('toggle')}, 3000)
      setTimeout(() => {commit('setMessage', null)}, 3000)
    },

    raiseInfo({commit}, payload) {
      commit('setColor', 'info');

      if (typeof payload === 'string') {
        commit('setMessage', payload);
      } else if (payload instanceof Error) {
        commit('setMessage', payload.response.data.message);
      } else if (typeof payload == 'object') {
        commit('setMessage', payload.message);
      }

      commit('toggle');
      setTimeout(() => {commit('toggle')}, 3000);
      setTimeout(() => {commit('setMessage', null)}, 3000);
    },

    raiseSuccess({commit}, payload) {
      commit('setColor', 'success');

      if (typeof payload === 'string') {
        commit('setMessage', payload);
      } else if (payload instanceof Error) {
        commit('setMessage', payload.response.data.message);
      } else if (typeof payload == 'object') {
        commit('setMessage', payload.message);
      }

      commit('toggle');
      setTimeout(() => {commit('toggle')}, 3000);
      setTimeout(() => {commit('setMessage', null)}, 3000);
    }
  },
  getters: {
    notificationMessage (state) {
      return state.message;
    },
    notificationColor (state) {
      return state.color;
    },
    notificationIsActive (state) {
      return Boolean(state.show);
    }
  }
}
