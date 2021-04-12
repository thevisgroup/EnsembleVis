<template>
  <div class="home">
    <b-container fluid>
      <div>
        <b-sidebar
          id="user-options"
          title="User Options"
          backdrop
          right
          shadow
          backdrop-variant="transparent"
          no-enforce-focus
        >
          <template #footer="{ hide }">
            <div class="d-flex bg-dark text-light px-3 py-2">
              <b-button size="md" @click="hide" variant="outline-light">Close</b-button>
            </div>
          </template>

          <b-card>
            <b-form>
              <label for="age_selected">Current Age Group: {{ options.age_selected }}</label>
              <b-form-input
                id="age_selected"
                v-model="options.age_selected"
                type="range"
                min="0"
                max="7"
                step="1"
              ></b-form-input>

              <hr />

              <b-form-checkbox
                v-model="options.show_selected_rows_only"
                id="show_selected_rows_only"
              >
                Show Selected Rows Only
              </b-form-checkbox>

              <b-form-checkbox v-model="options.show_matrix" id="show_matrix">
                Show Scatterplot
              </b-form-checkbox>

              <b-form-checkbox v-model="options.table.showAvgLine" id="options.table.showAvgLine">
                Show Average Marker
              </b-form-checkbox>
            </b-form>
          </b-card>
        </b-sidebar>
      </div>

      <b-row>
        <b-col cols="8">
          <ParallelCoordinates></ParallelCoordinates>

          <PCOut
            :data="{
              age_selected: options.age_selected,
              simulation_selected: options.simulation_selected,
            }"
          ></PCOut>
        </b-col>

        <b-col cols="4">
          <b-row>
            <b-col cols="12"> </b-col>
          </b-row>

          <b-row class="mt-2">
            <b-col cols="12">
              <LineChart
                :data="{
                  age_selected: options.age_selected,
                  simulation_selected: options.simulation_selected,
                }"
              ></LineChart>

              <!-- <Umap
                :data="{
                  age_selected: options.age_selected,
                  simulation_selected: options.simulation_selected,
                }"
              ></Umap> -->

              <!-- <PCA
                :data="{
                  age_selected: options.age_selected,
                }"
              ></PCA> -->
              <PCA></PCA>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row v-if="options.show_matrix">
        <Matrix></Matrix>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import { mapState } from "vuex";
import PCA from "../components/PCA.vue";

export default {
  data() {
    return {};
  },
  components: {
    PCA,
  },
  methods: {
    generateAge() {
      let res = [];
      for (let index = 0; index < 8; index++) {
        res.push({ value: index, text: index });
      }
      return res;
    },
  },
  watch: {},
  computed: {
    ...mapState(["options"]),
  },
  mounted() {},
};
</script>
