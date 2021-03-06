import Vue from "vue";
import Vuex from "vuex";
Vue.use(Vuex);
import store from "./store";

import { BootstrapVue, BootstrapVueIcons } from "bootstrap-vue";
import App from "./App.vue";
import router from "./router";

Vue.use(BootstrapVue);
import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";
Vue.use(BootstrapVueIcons);

import ParallelCoordinates from "./components/ParallelCoordinates.vue";
Vue.component("ParallelCoordinates", ParallelCoordinates);

import PCOut from "./components/PCOut.vue";
Vue.component("PCOut", PCOut);

import Umap from "./components/Umap.vue";
Vue.component("Umap", Umap);

import LineChart from "./components/LineChart.vue";
Vue.component("LineChart", LineChart);

import Matrix from "./components/Matrix.vue";
Vue.component("Matrix", Matrix);

Vue.config.productionTip = false;

new Vue({
  el: "#app",
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
