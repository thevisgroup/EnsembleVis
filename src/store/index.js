import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const options = {
  namespaced: true,
  state: {
    simulation_selected: 0,
    age_selected: 0,
  },
  mutations: {},
  getters: {},
};

export default new Vuex.Store({
  modules: {
    options,
  },
});
