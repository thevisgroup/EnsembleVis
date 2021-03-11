<template>
  <div class="home">
    <b-container fluid>
      <b-row>
        <b-col cols="8">
          <ParallelCoordinates></ParallelCoordinates>
        </b-col>

        <b-col cols="4">
          <b-row>
            <b-col cols="12">
              <b-card header="User options">
                <b-form>
                  <!-- <b-form-group label="Age Group" label-for="select_age">
                    <b-form-select
                      id="select_age"
                      v-model="options.age_selected"
                      :options="generateAge()"
                    ></b-form-select>
                  </b-form-group> -->

                  <label for="age_selected">Show Age Group: {{ options.age_selected }}</label>
                  <b-form-input
                    id="age_selected"
                    v-model="options.age_selected"
                    type="range"
                    min="0"
                    max="7"
                    step="1"
                  ></b-form-input>

                  <b-form-checkbox v-model="show_matrix" id="show_matrix">
                    Show Scatterplot
                  </b-form-checkbox>
                  <!-- <label for="select_iter">Day: {{ day_selected }}</label>
                  <b-form-input
                    id="select_iday"
                    v-model="day_selected"
                    type="range"
                    min="1"
                    max="200"
                    step="1"
                  ></b-form-input> -->
                </b-form>
              </b-card>
            </b-col>
          </b-row>

          <b-row class="mt-2">
            <b-col cols="12">
              <LineChart
                :data="{
                  age_selected: options.age_selected,
                  simulation_selected: options.simulation_selected,
                }"
              ></LineChart>
            </b-col>
          </b-row>
        </b-col>
      </b-row>
      <b-row>
        <b-col cols="8">
          <PCOut
            :data="{
              age_selected: options.age_selected,
              simulation_selected: options.simulation_selected,
            }"
          ></PCOut>
        </b-col>
        <b-col cols="4">
          <Umap
            :data="{
              age_selected: options.age_selected,
              simulation_selected: options.simulation_selected,
            }"
          ></Umap>
        </b-col>
      </b-row>
      <b-row v-if="show_matrix">
        <Matrix></Matrix>
      </b-row>
    </b-container>
  </div>
</template>
<script>
import { mapState } from "vuex";
export default {
  data() {
    return {
      show_matrix: false,
    };
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
