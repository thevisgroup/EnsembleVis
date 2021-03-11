<template>
  <div>
    <div id="umap"></div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "Umap",
  props: ["data"],
  data() {
    return {
      umapdata: null,
    };
  },
  methods: {
    async load() {
      const __VM = this;

      d3.selectAll("#umap > svg").remove();

      __VM.umapdata = await d3.csv(
        `/assets/data/output/umap/d/age_${__VM.data.age_selected}.csv`,
        d3.autoType
      );

      const margin = { top: 30, right: 30, bottom: 30, left: 30 };
      const width = window.innerWidth / 3 - margin.left - margin.right;
      const height = window.innerHeight / 2 + margin.top + margin.bottom;
      // const height = window.innerHeight / 1.5 - margin.top - margin.bottom;
      const svg = d3
        .select("#umap")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr(
          "viewBox",
          `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`
        )
        .attr("preserveAspectRatio", "xMinYMin")
        .append("g");

      const color = d3.scaleSequential(d3.interpolateTurbo);

      svg.append("style").text(`circle.hidden { fill: grey;}`);
      const x = d3
        .scaleLinear()
        .domain(d3.extent(__VM.umapdata, (d) => d["umap-2d-one"]))
        .range([margin.left, width - margin.right]);
      const xAxis = (g) =>
        g
          .call(d3.axisBottom(x))
          .attr("transform", `translate(0,${height + margin.top * 1.2})`)
          .call((g) => g.select(".domain").remove())
          .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));

      svg.append("g").call(xAxis);

      const y = d3
        .scaleLinear()
        .domain(d3.extent(__VM.umapdata, (d) => d["umap-2d-two"]))
        .range([margin.left, width - margin.right]);

      const yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y))
          .call((g) => g.select(".domain").remove())
          .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));

      svg.append("g").call(yAxis);

      const dot = svg
        .append("g")
        .selectAll("circle")
        .data(__VM.umapdata)
        .join("circle")
        .attr("transform", (d) => `translate(${x(d["umap-2d-one"])},${y(d["umap-2d-two"])})`)
        .attr("fill", (d) => color(parseInt(d["y_sub"]) / 9))
        .attr("r", 3);

      const brush = d3.brush().on("brush end", brushed);

      svg.call(brush);

      function brushed({ selection }) {
        let selected = [];
        if (selection) {
          const [[x0, y0], [x1, y1]] = selection;

          dot.classed(
            "hidden",
            (d) =>
              x0 > x(d["umap-2d-one"]) ||
              x(d["umap-2d-one"]) > x1 ||
              y0 > y(d["umap-2d-two"]) ||
              y(d["umap-2d-two"]) > y1
          );

          selected = dot
            .filter(
              (d) =>
                x0 < x(d["umap-2d-one"]) &&
                x1 > x(d["umap-2d-one"]) &&
                y0 < y(d["umap-2d-two"]) &&
                y1 > y(d["umap-2d-two"])
            )
            .data();
        } else {
          dot.classed("hidden", false);
        }
        svg.property("value", selected).dispatch("input");
      }

      return Promise.resolve();
    },
  },
  async mounted() {
    const __VM = this;
    await __VM.load();
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

<style></style>
