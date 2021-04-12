import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);

const options = {
  namespaced: true,
  state: {
    simulation_selected: 0,
    age_selected: 0,
    show_matrix: false,
    show_selected_rows_only: false,
    table: {
      showAvgLine: true,
      initData: [],
      selectedRows: [],
    },
  },
  mutations: {},
  getters: {
    isRowSelected: (state) => (id) => {
      return state.table.selectedRows.filter((d) => d.Index === id).length > 0;
    },
  },
};

export default new Vuex.Store({
  modules: {
    options,
  },
});
