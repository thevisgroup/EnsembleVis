import Vue from "vue";
import Router from "vue-router";
import Home from "./views/Home.vue";

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
    },
    {
      path: "/SomeView",
      name: "SomeView",
      component: () => import("./views/SomeView.vue"),
    },
  ],
});
