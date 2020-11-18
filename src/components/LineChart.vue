<template>
  <div>
    <div id="lineChart"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
// import { mapState } from "vuex";

export default {
  name: "LineChart",
  props: ["data"],
  computed: {},
  data() {
    return {
      chartData: {
        data: null,
        dimensions: null,
      },
      key: 0,
    };
  },
  methods: {
    draw() {
      const __VM = this;

      const { data, dimensions } = __VM.chartData;

      d3.selectAll("#lineChart > svg").remove();

      const margin = { top: 30, right: 40, bottom: 30, left: 40 };
      const width = window.innerWidth / 3 - margin.left - margin.right;
      const height = window.innerHeight / 2 - margin.top - margin.bottom;

      // eslint-disable-next-line no-unused-vars
      const svg = d3
        .select("#lineChart")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr(
          "viewBox",
          `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`
        )
        .attr("preserveAspectRatio", "xMinYMin")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      const x = d3.scaleLinear().domain([0, data.length]).range([0, width]);

      svg
        .append("g")
        .attr("transform", `translate(${margin.left},${height})`)
        .call(d3.axisBottom(x));

      const population_y = d3.scaleLinear().domain([1300000, 0]).range([0, height]);
      // the actual population, according to the simulation log, is 5438100

      svg
        .append("g")
        .attr("transform", `translate(${margin.left},0)`)
        .call(d3.axisLeft(population_y))
        .append("text")
        .attr("class", "xLabel")
        .attr("dy", "-1em")
        .attr("fill", "black")
        .style("text-anchor", "end")
        .text("Pupolation");

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      // Generate mutlt Y axes
      // let yAxes = {};

      // dimensions.forEach((dimension) => {
      // let y = d3
      //   .scaleLinear()
      //   .range([height, 0])
      //   .domain([
      //     0,
      //     d3.max(data, function (c) {
      //       return +c[dimension];
      //     }),
      //   ]);
      // yAxes[dimension] = y;
      // svg
      //   .append("g")
      //   .attr("transform", `translate(-${i * 40},0)`)
      //   .call(d3.axisLeft(y))
      //   .append("text")
      //   .attr("class", "axisLabel")
      //   .attr("y", -16)
      //   .attr("dy", "0.8em")
      //   .attr("fill", color(i))
      //   .style("text-anchor", "end")
      //   .text(dimension);
      // });

      // Draw confidence interval
      // svg
      //   .append("path")
      //   .datum(data)
      //   .attr("fill", "#cce5df")
      //   .attr("stroke", "none")
      //   .attr(
      //     "d",
      //     d3
      //       .area()
      //       .x(function (d, i) {
      //         return x(i);
      //       })
      //       .y0(function (d) {
      //         return yAxes.D(+d.D * 1.1);
      //       })
      //       .y1(function (d) {
      //         return yAxes.D(+d.D * 0.8);
      //       })
      //   );

      // Draw lines
      dimensions.forEach((dimension, i) => {
        svg
          .append("path")
          .attr("class", "lines")
          .datum(data)
          .attr("transform", `translate(${margin.left},0)`)
          .attr("fill", "none")
          .attr("stroke", color(i))
          .attr("stroke-width", 1.5)
          // .attr("d", path);
          .attr(
            "d",
            d3
              .line()
              .x(function (d, i) {
                return x(i);
              })
              .y(function (d) {
                return population_y(+d[dimension]);
                // return yAxes[dimension](+d[dimension]);
              })
          );
      });

      // Generate color legends
      dimensions.forEach((dimension, i) => {
        svg
          .append("rect")
          .attr("x", width - margin.right * 2)
          .attr("y", i * 20)
          .attr("width", 10)
          .attr("height", 10)
          .style("fill", color(i));

        svg
          .append("text")
          .attr("x", width - margin.right * 1.5)
          .attr("y", i * 20 + 10)
          .text(dimension);
      });
    },
    async load() {
      this.chartData.data = await d3.csv(
        `/assets/data/out/${this.data.age_group}/${this.data.day - 1}.csv`
      );

      this.chartData.dimensions = Object.keys(this.chartData.data[0]);

      this.draw();
    },
  },
  async mounted() {
    const __VM = this;
    await this.load();

    let resizeTimer;
    d3.select(window).on("resize", async () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(async () => {
        await __VM.draw();
      }, 250);
    });
  },
  watch: {
    data: {
      deep: true,
      handler: function () {
        this.load();
      },
    },
  },
};
</script>

<style>
.xLabel {
  font-weight: bolder;
  font-size: 1.5em;
}

text[fill="currentColor"] {
  font-size: 1.2em;
}
</style>
