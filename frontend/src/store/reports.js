import { stat } from "fs";

export default {
    state: {
        filters: [],
        params: []
    },

    mutations: {
        setFilters (state, payload) {
            state.filters = payload
        },
        setParams (state, payload) {
            state.params = payload
        }
    },

    actions: {
        setReportFilters ({commit}, payload) {
            commit('setFilters', payload)
        },
        setReportParams ({commit}, payload) {
            commit('setParams', payload)
        }
    },

    getters: {
        reportFilters (state) {
            return state.filters
        },
        reportParams (state) {
            return state.params
        }
    }
}