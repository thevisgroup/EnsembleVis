<template>
  <div>
    <div id="PCA"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapState } from "vuex";

export default {
  name: "PCA",
  props: ["data"],
  computed: {
    ...mapState(["options"]),
  },
  data() {
    return {
      PCAdata: null,
    };
  },
  methods: {
    async init() {
      const __VM = this;

      d3.selectAll("#PCA > svg").remove();

      // __VM.PCAdata = await d3.csv(
      //   `/assets/data/output/pca/d/age_${__VM.data.age_selected}.csv`,
      //   d3.autoType
      // );

      __VM.PCAdata = await d3.csv(`/assets/data/output/pca/d/age_mean.csv`, d3.autoType);

      const yMin = d3.min(__VM.PCAdata, (d) => d.y);
      const yMax = d3.max(__VM.PCAdata, (d) => d.y);

      const colorScale = yMax + Math.abs(yMin);

      const margin = { top: 30, right: 30, bottom: 30, left: 30 };
      const width = window.innerWidth / 3 - margin.left - margin.right;
      const height = window.innerHeight / 2 + margin.top + margin.bottom;
      // const height = window.innerHeight / 1.5 - margin.top - margin.bottom;
      const svg = d3
        .select("#PCA")
        .append("svg")
        .attr("width", "100%")
        .attr("height", "100%")
        .attr(
          "viewBox",
          `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`
        )
        .attr("preserveAspectRatio", "xMinYMin")
        .append("g")
        .attr("transform", `translate(0,${margin.top})`);

      // eslint-disable-next-line no-unused-vars
      const color = d3.scaleSequential(d3.interpolateTurbo);

      svg.append("style").text(`circle.hidden { fill: #e3e3e3;}`);
      const x = d3
        .scaleLinear()
        .domain(d3.extent(__VM.PCAdata, (d) => d["x"]))
        .range([margin.left, width + margin.left]);
      const xAxis = (g) =>
        g
          .call(d3.axisBottom(x).ticks(20))
          .attr("transform", `translate(0,${height})`)
          .call((g) => g.select(".domain").remove())
          .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));

      const y = d3
        .scaleLinear()
        .domain(d3.extent(__VM.PCAdata, (d) => d["y"]))
        .range([height, margin.top / 2]);

      const yAxis = (g) =>
        g
          .attr("transform", `translate(${margin.left},0)`)
          .call(d3.axisLeft(y).ticks(20))
          .call((g) => g.select(".domain").remove())
          .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));
      console.log(__VM.options.table.selectedRows);
      const dot = svg
        .append("g")
        .selectAll("circle")
        .data(__VM.PCAdata.reverse())
        .join("circle")
        .attr("transform", (d) => `translate(${x(d["x"])},${y(d["y"])})`)
        // .attr("fill", color(parseInt(__VM.data.age_selected) + 1 / 9))
        .attr("fill", (d) =>
          d.y >= 0
            ? color((d.y + Math.abs(yMin)) / colorScale)
            : color(Math.abs(yMin - d.y) / colorScale)
        )
        .attr("class", (d) => {
          if (!__VM.options.table.selectedRows.some((x) => x.Index === d.simu)) {
            return "hidden";
          }
        })
        // for aggregated age_group
        // .attr("fill", (d) =>
        //   d.age_group === parseInt(__VM.data.age_selected) ? "rgb(8, 82, 35)" : "#e3e3e3"
        // )
        // .attr("fill-opacity", (d) => (d.age_group === parseInt(__VM.data.age_selected) ? 1 : 0.8))
        .attr("r", 3);

      svg.append("g").call(xAxis);
      svg.append("g").call(yAxis);

      const brush = d3.brush().on("brush", brushStart).on("end", brushEnd);

      svg.call(brush);
      let selected = [];
      function brusher({ selection }) {
        selected = [];
        if (selection) {
          const [[x0, y0], [x1, y1]] = selection;

          dot.classed(
            "hidden",
            (d) => x0 > x(d["x"]) || x(d["x"]) > x1 || y0 > y(d["y"]) || y(d["y"]) > y1
          );

          selected = dot
            .filter((d) => x0 < x(d["x"]) && x1 > x(d["x"]) && y0 < y(d["y"]) && y1 > y(d["y"]))
            .data();
        } else {
          dot.classed("hidden", false);
        }
      }

      function brushStart({ selection }) {
        brusher({ selection });
      }
      function brushEnd({ selection }) {
        brusher({ selection });

        // selected = selected
        //   .filter((s) => s.age_group === parseInt(__VM.data.age_selected))
        //   .map((d) => d.simu);

        selected = selected.map((d) => d.simu);

        if (selected.length > 0) {
          __VM.options.table.selectedRows = __VM.options.table.initData.filter(
            (s) => selected.includes(s.Index) || __VM.options.simulation_selected === s.Index
          );
        } else {
          __VM.options.table.selectedRows = __VM.options.table.initData;
        }

        // trigger PCP redraw
        __VM.options.pcp.count++;
      }

      return Promise.resolve();
    },
  },
  async mounted() {
    this.init();
  },
  watch: {
    "options.pca.count": {
      handler: function () {
        this.init();
      },
    },
  },
};
</script>

<style></style>
