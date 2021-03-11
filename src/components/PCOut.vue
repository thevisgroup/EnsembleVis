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
      const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight / 1.5 - margin.top - margin.bottom;

      const x = d3.scalePoint().range([0, width]).padding(1);
      const y = {};

      const colorScheme = d3.interpolateTurbo;
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
        (__VM.dimensions = Object.keys(__VM.data.pcdata[0]).filter((d) => {
          return (
            !d.includes("min") &&
            !d.includes("max") &&
            (y[d] = d3
              .scaleLinear()
              .domain(
                d3.extent(__VM.data.pcdata, function (p) {
                  return +p[d];
                })
              )
              .range([height, 0]))
          );
        }))
      );

      let colors = {};
      Object.keys(__VM.data.pcdata[0]).map((d) => {
        colors[d] = d3
          .scaleSequential()
          .domain(
            d3.extent(__VM.data.pcdata, function (d) {
              return +d[name];
            })
          )
          .interpolator(colorScheme);
      });

      // Add grey background lines for context.
      // eslint-disable-next-line no-unused-vars
      background = svg
        .append("g")
        .attr("class", "background")
        .selectAll("path")
        .data(__VM.data.pcdata)
        .enter()
        .append("path")
        .attr("d", path);

      // Add blue foreground lines for focus.
      foreground = svg
        .append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(__VM.data.pcdata)
        .enter()
        .append("path")
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
