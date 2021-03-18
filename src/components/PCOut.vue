<template>
  <div>
    <div id="parallelCoordinatesOutput"></div>
  </div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "ParallelCoordinatesOutput",
  props: ["data"],
  data() {
    return {
      dimensions: [],
    };
  },
  methods: {
    async load() {
      const __VM = this;

      // eslint-disable-next-line vue/no-mutating-props
      __VM.data.pcdata = await d3.csv(
        `/assets/data/output/simu_${__VM.data.simulation_selected}/age_${__VM.data.age_selected}.csv`,
        d3.autoType
      );

      let avgPolylines = await d3.csv(
        `/assets/data/output/simu_${__VM.data.simulation_selected}/avgPolyline.csv`,
        d3.autoType
      );
      // add age_group axis
      // eslint-disable-next-line vue/no-mutating-props
      __VM.data.pcdata.columns.unshift("age_group");
      __VM.data.pcdata.forEach((i) => (i["age_group"] = __VM.data.age_selected));

      // add isAvg for highlighting
      // eslint-disable-next-line vue/no-mutating-props
      __VM.data.pcdata.columns.push("isAvg");
      __VM.data.pcdata.forEach((i) => (i["isAvg"] = false));
      avgPolylines.columns.push("isAvg");
      avgPolylines.forEach((i) => (i["isAvg"] = true));

      const data = [...__VM.data.pcdata, ...avgPolylines];
      data.columns = avgPolylines.columns;

      const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight / 1.5 - margin.top - margin.bottom;

      const x = d3.scalePoint().range([0, width]).padding(1);
      const y = {};

      const axis = d3.axisLeft();

      let background, foreground;

      const svg = d3
        .select("#parallelCoordinatesOutput")
        .append("svg")
        .attr("class", `pcout_${__VM.data.simulation_selected}_${__VM.data.age_selected}`)
        .attr("width", "100%")
        .attr("height", "100%")
        .attr(
          "viewBox",
          `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`
        )
        .attr("preserveAspectRatio", "xMinYMin")
        .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

      d3.selectAll(
        `#parallelCoordinatesOutput > svg:not(.pcout_${__VM.data.simulation_selected}_${__VM.data.age_selected})`
      ).remove();

      // Extract the list of dimensions and create a scale for each.
      x.domain(
        (__VM.dimensions = data.columns.filter((d) => {
          return (
            !d.includes("min") &&
            !d.includes("max") &&
            !d.includes("isAvg") &&
            (y[d] = d3
              .scaleLinear()
              .domain(d3.extent(data, (p) => +p[d]))
              .range([height, 10]))
          );
        }))
      );

      const color = d3.scaleSequential(d3.interpolateTurbo);

      // Add grey background lines for context.
      // eslint-disable-next-line no-unused-vars
      background = svg
        .append("g")
        .attr("class", "background")
        .selectAll("path")
        .data(data)
        .enter()
        .append("path")
        .attr("d", path);

      let defs = svg.append("defs");

      // dot for average polylines
      const avgPolylineDot = (color) => {
        let id = color.replace(/\D+/g, "");
        defs
          .append("marker")
          .attr("id", id)
          .attr("viewBox", [0, 0, 20, 20])
          .attr("refX", 10)
          .attr("refY", 10)
          .attr("markerWidth", 4)
          .attr("markerHeight", 4)
          .append("circle")
          .attr("cx", 10)
          .attr("cy", 10)
          .attr("r", 10)
          .style("fill", color);

        return "url(#" + id + ")";
      };

      // Add blue foreground lines for focus.
      foreground = svg
        .append("g")
        // .attr("class", "foreground")
        .selectAll("path")
        .data(data)
        .enter()
        .append("path")
        .attr("stroke", (d) => (d["isAvg"] ? color(parseInt(d["age_group"]) / 9) : "steelblue"))
        .attr("stroke-width", (d) => (d["isAvg"] ? "3" : "1"))
        .attr("fill", "none")
        .attr("marker-mid", (d) =>
          d["isAvg"] ? avgPolylineDot(color(parseInt(d["age_group"]) / 9)) : ""
        )
        .attr("d", path);

      // Add a group element for each dimension.
      const g = svg
        .selectAll(".dimension")
        .data(__VM.dimensions)
        .enter()
        .append("g")
        .attr("class", "dimension")
        .attr("transform", (d) => "translate(" + x(d) + ")");

      // Add an axis and title.
      g.append("g")
        .attr("class", "axis")
        .each(function (d) {
          if (d === "age_group") {
            axis.ticks(8);
          }
          d3.select(this).call(axis.scale(y[d]));
        })
        .append("text")
        .attr("class", "yLabel")
        .style("text-anchor", "middle")
        .attr("y", -9)
        .text((d) => d);

      // Add and store a brush for each axis.
      g.append("g")
        .attr("class", "brush")
        .each(function (d) {
          d3.select(this).call(
            (y[d].brush = d3
              .brushY()
              .extent([
                [-10, 0],
                [10, height],
              ])
              .on("brush", brush)
              .on("end", brush))
          );
        })
        .selectAll("rect")
        .attr("x", -8)
        .attr("width", 16);

      // Returns the path for a given data point.
      function path(d) {
        const res = d3.line()(
          __VM.dimensions.map(function (p) {
            return [x(p), y[p](d[p])];
          })
        );
        return res;
      }

      // Handles a brush event, toggling the display of foreground lines.
      function brush() {
        const actives = [];
        svg
          .selectAll(".brush")
          .filter(function (d) {
            y[d].brushSelectionValue = d3.brushSelection(this);
            return d3.brushSelection(this);
          })
          .each(function (d) {
            // Get extents of brush along each active selection axis (the Y axes)
            actives.push({
              dimension: d,
              extent: d3.brushSelection(this).map(y[d].invert),
            });
          });

        let local_selected = [];
        // Update foreground to only display selected values
        foreground.style("display", function (d) {
          return actives.every(function (active) {
            let result =
              active.extent[1] <= d[active.dimension] && d[active.dimension] <= active.extent[0];
            if (result) {
              local_selected.push(d);
            }
            return result;
          })
            ? null
            : "none";
        });

        const display = [];
        local_selected.forEach((l) => {
          if (local_selected.filter((s) => s.Index === l.Index).length === actives.length) {
            display.push(l);
          }
        });

        return Promise.resolve();
      }
    },
  },
  async mounted() {
    const __VM = this;
    await __VM.load();

    let resizeTimer;
    d3.select(window).on("resize", async () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(async () => {
        await __VM.load();
      }, 250);
    });
  },
  watch: {
    "data.simulation_selected": {
      handler: function () {
        this.load();
      },
    },
    "data.age_selected": {
      handler: function () {
        this.load();
      },
    },
  },
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
</style>
