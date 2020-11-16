<template>
  <div class="home">
    <b-container fluid>
      <b-row>
        <b-col cols="4">
          <b-row>
            <b-col cols="12">
              <b-card header="User options">
                <b-form>
                  <!-- <b-form-group label="Age Group" label-for="select_age">
                    <b-form-select
                      id="select_age"
                      v-model="age_selected"
                      :options="generateAge()"
                    ></b-form-select>
                  </b-form-group> -->

                  <label for="select_iter">Age Group: {{ age_selected }}</label>
                  <b-form-input
                    id="age_selected"
                    v-model="age_selected"
                    type="range"
                    min="0"
                    max="7"
                    step="1"
                  ></b-form-input>

                  <label for="select_iter">Iteration: {{ iter_selected }}</label>
                  <b-form-input
                    id="select_iter"
                    v-model="iter_selected"
                    type="range"
                    min="1"
                    max="200"
                    step="1"
                  ></b-form-input>
                </b-form>
              </b-card>
            </b-col>
          </b-row>

          <b-row class="mt-2">
            <b-col cols="12">
              <LineChart :data="{ age_group: age_selected, iteration: iter_selected }"></LineChart>
            </b-col>
          </b-row>
        </b-col>

        <b-col cols="8">
          <ParallelCoordinates></ParallelCoordinates>
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>
<script>
export default {
  data() {
    return {
      age_selected: 0,
      iter_selected: 1,
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
  computed: {},
  mounted() {},
};
</script>
