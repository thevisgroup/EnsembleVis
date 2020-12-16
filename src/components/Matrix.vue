<template>
  <div>
    <div id="matrix"></div>
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapState } from "vuex";

export default {
  name: "Matrix",
  computed: {
    ...mapState(["options"]),
  },
  data() {
    return {
      rowsToDisplay: 160,
      dimensions: [],
      data: null,
      tableData: [],
      headers: [],
    };
  },
  methods: {
    async init() {
      const __VM = this;

      d3.selectAll("#matrix > svg").remove();

      __VM.data = await d3.csv("/assets/posterior_parameters.csv", d3.autoType);

      const columns = Object.keys(__VM.data[0])
        .filter((d) => d !== "Index" && d !== "rrd" && d !== "K")
        .splice(0, 5);

      // const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const padding = 20;
      const width = window.innerWidth / 2;
      const size = (width - (columns.length + 1) * padding) / columns.length + padding;
      // const height = window.innerHeight / 1.5 - margin.top - margin.bottom;
      const svg = d3
        .select("#matrix")
        .append("svg")
        .attr("width", `${width}px`)
        .attr("height", `${width}px`)
        .attr("viewBox", [-padding, 0, width, width])
        .attr("preserveAspectRatio", "xMinYMin");

      svg.append("style").text(`circle.hidden { fill: #000; fill-opacity: 1; r: 1px; }`);

      const x = columns.map((c) =>
        d3
          .scaleLinear()
          .domain(d3.extent(__VM.data, (d) => d[c]))
          .rangeRound([padding / 2, size - padding / 2])
      );

      const xAxis = () => {
        const axis = d3
          .axisBottom()
          .ticks(6)
          .tickSize(size * columns.length);
        return (g) =>
          g
            .selectAll("g")
            .data(x)
            .join("g")
            .attr("transform", (d, i) => `translate(${i * size},0)`)
            .each(function (d) {
              return d3.select(this).call(axis.scale(d));
            })
            .call((g) => g.select(".domain").remove())
            .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));
      };

      svg.append("g").call(xAxis());

      const y = x.map((x) => x.copy().range([size - padding / 2, padding / 2]));

      const yAxis = () => {
        const axis = d3
          .axisLeft()
          .ticks(6)
          .tickSize(-size * columns.length);

        return (g) =>
          g
            .selectAll("g")
            .data(y)
            .join("g")
            .attr("transform", (d, i) => `translate(0,${i * size})`)
            .each(function (d) {
              return d3.select(this).call(axis.scale(d));
            })
            .call((g) => g.select(".domain").remove())
            .call((g) => g.selectAll(".tick line").attr("stroke", "#ddd"));
      };

      svg.append("g").call(yAxis());

      const z = d3.scaleSequential(d3.interpolatePiYG);

      const cell = svg
        .append("g")
        .selectAll("g")
        .data(d3.cross(d3.range(columns.length), d3.range(columns.length)))
        .join("g")
        .attr("transform", ([i, j]) => `translate(${i * size},${j * size})`);

      cell
        .append("rect")
        .attr("fill", "none")
        .attr("stroke", "#aaa")
        .attr("x", padding / 2 + 0.5)
        .attr("y", padding / 2 + 0.5)
        .attr("width", size - padding)
        .attr("height", size - padding);

      cell.each(function ([i, j]) {
        d3.select(this)
          .selectAll("circle")
          .data(__VM.data.filter((d) => !isNaN(d[columns[i]]) && !isNaN(d[columns[j]])))
          .join("circle")
          .attr("cx", (d) => x[i](d[columns[i]]))
          .attr("cy", (d) => y[j](d[columns[j]]));
      });

      const circle = cell
        .selectAll("circle")
        .attr("r", 3.5)
        .attr("fill-opacity", 0.7)
        .attr("fill", (d) => z(d.Index / __VM.data.length));

      cell.call(brush, circle, svg);

      svg
        .append("g")
        .style("font", "bold 10px sans-serif")
        .style("pointer-events", "none")
        .selectAll("text")
        .data(columns)
        .join("text")
        .attr("transform", (d, i) => `translate(${i * size},${i * size})`)
        .attr("x", padding)
        .attr("y", padding)
        .attr("dy", ".71em")
        .text((d) => d);

      svg.property("value", []);

      function brush(cell, circle, svg) {
        const brush = d3
          .brush()
          .extent([
            [padding / 2, padding / 2],
            [size - padding / 2, size - padding / 2],
          ])
          .on("start", brushstarted)
          .on("brush", brushed)
          .on("end", brushended);

        cell.call(brush);

        let brushCell;

        // Clear the previously-active brush, if any.
        function brushstarted() {
          if (brushCell !== this) {
            d3.select(brushCell).call(brush.move, null);
            brushCell = this;
          }
        }

        // Highlight the selected circles.
        function brushed({ selection }, [i, j]) {
          let selected = [];
          if (selection) {
            const [[x0, y0], [x1, y1]] = selection;
            circle.classed(
              "hidden",
              (d) =>
                x0 > x[i](d[columns[i]]) ||
                x1 < x[i](d[columns[i]]) ||
                y0 > y[j](d[columns[j]]) ||
                y1 < y[j](d[columns[j]])
            );
            selected = __VM.data.filter(
              (d) =>
                x0 < x[i](d[columns[i]]) &&
                x1 > x[i](d[columns[i]]) &&
                y0 < y[j](d[columns[j]]) &&
                y1 > y[j](d[columns[j]])
            );
          }
          svg.property("value", selected).dispatch("input");
        }

        // If the brush is empty, select all circles.
        function brushended({ selection }) {
          if (selection) return;
          svg.property("value", []).dispatch("input");
          circle.classed("hidden", false);
        }
      }

      return Promise.resolve();
    },
  },
  async mounted() {
    const __VM = this;
    await __VM.init();

    // let resizeTimer;
    // d3.select(window).on("resize", async () => {
    //   clearTimeout(resizeTimer);
    //   resizeTimer = setTimeout(async () => {
    //     await __VM.init();
    //   }, 250);
    // });
  },
  watch: {},
};
</script>

<style>
svg {
  font: 1.2rem;
}

.background path {
  fill: none;
  stroke: #ddd;
  shape-rendering: crispEdges;
}

.foreground path {
  fill: none;
  stroke: steelblue;
}

.brush .extent {
  fill-opacity: 0.3;
  stroke: #fff;
  shape-rendering: crispEdges;
}

.axis line,
.axis path {
  fill: none;
  stroke: #000;
  shape-rendering: crispEdges;
}

.axis text {
  fill: black;
  text-shadow: 0 1px 0 #fff, 1px 0 0 #fff, 0 -1px 0 #fff, -1px 0 0 #fff;
  font-size: 1.2rem !important;
}

.axis .yLabel {
  font-weight: bolder;
  font-size: 1.4rem !important;
}

table {
  font-size: 0.8rem !important;
}
</style>
