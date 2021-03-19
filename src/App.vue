<template>
  <div id="app">
    <b-navbar toggleable="lg" type="light" variant="light" class="sticky-top">
      <b-navbar-brand to="/">
        <b-img src="./assets/icon-nav.svg"></b-img>
      </b-navbar-brand>
      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav class="ml-auto">
          <!-- <b-nav-item to="/">Home</b-nav-item>
          <b-nav-item to="/ParallelCoordinates">Parallel Coordinates</b-nav-item> -->
          <li class="my-auto">
            <label for="age_selected">Current Age Group: {{ options.age_selected }}</label>
            <b-input
              id="age_selected"
              v-model="options.age_selected"
              type="range"
              min="0"
              max="7"
              step="1"
            ></b-input>
          </li>
          <li class="my-auto">
            <b-checkbox v-model="options.show_matrix" id="show_matrix">
              Show Scatterplot
            </b-checkbox>
          </li>
          <li class="my-auto ml-5">
            <b-button v-b-toggle.user-options>Option Sidebar</b-button>
          </li>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>

    <router-view />
  </div>
</template>

<script>
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState(["options"]),
  },
};
</script>

<style>
body {
  font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica Neue, Arial, Noto Sans,
    sans-serif, Apple Color Emoji, Segoe UI Emoji, Segoe UI Symbol, Noto Color Emoji;
  font-size: 1.1rem;
}

nav {
  margin-bottom: 1em;
  font-weight: 600;
}

.custom-range {
  width: 70% !important;
}
</style>
