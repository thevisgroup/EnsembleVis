import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const colorScheme = {
  namespaced: true,
  state: {
    scheme: [
      "#68b0fc",
      "#265581",
      "#55af79",
      "#30693c",
      "#aee64f",
      "#ff9149",
      "#e4ad82",
      "#922d18",
      "#f85e17",
      "#29f385",
      "#81174c",
      "#f07796",
      "#ff0085",
      "#e9d737",
    ],
  },
  mutations: {},
  getters: {},
};

export default new Vuex.Store({
  modules: {
    colorScheme,
  },
});
