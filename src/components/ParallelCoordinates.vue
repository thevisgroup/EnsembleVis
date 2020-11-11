<template>
  <b-col cols="11">
    <div id="parallelCoordinates"></div>
    <pre></pre>
  </b-col>
</template>

<script>
import * as d3 from "d3";
// import { mapState } from "vuex";

export default {
  name: "ParallelCoordinates",
  computed: {},
  data() {
    return {};
  },
  methods: {
    async init() {
      d3.selectAll("#parallelCoordinates > svg").remove();

      const data = await d3.csv("/assets/posterior_parameters.csv");

      const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight / 1.5 - margin.top - margin.bottom;

      const x = d3.scalePoint().range([0, width]).padding(1);
      const y = {};

      const colorScheme = d3.interpolateTurbo;
      const axis = d3.axisLeft();

      let background, foreground, dimensions;

      const svg = d3
        .select("#parallelCoordinates")
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

      // Extract the list of dimensions and create a scale for each.
      x.domain(
        (dimensions = Object.keys(data[0]).filter(function (d) {
          return (
            d !== "Index" &&
            d !== "rrd" &&
            d !== "K" &&
            (y[d] = d3
              .scaleLinear()
              .domain(
                d3.extent(data, function (p) {
                  return +p[d];
                })
              )
              .range([height, 0]))
          );
        }))
      );

      let colors = {};
      Object.keys(data[0]).map((d) => {
        colors[d] = d3
          .scaleSequential()
          .domain(
            d3.extent(data, function (d) {
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
        .data(data)
        .enter()
        .append("path")
        .attr("d", path);

      // Add blue foreground lines for focus.
      foreground = svg
        .append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(data)
        .enter()
        .append("path")
        .attr("d", path);

      // Add a group element for each dimension.
      const g = svg
        .selectAll(".dimension")
        .data(dimensions)
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
          dimensions.map(function (p) {
            return [x(p), y[p](d[p])];
          })
        );
        return res;
      }

      let out = d3.select("pre");
      out.text(d3.tsvFormat(data.slice(0, 24)));

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

        actives.length > 0
          ? out.text(d3.tsvFormat([...new Set(display)].slice(0, 24)))
          : out.text(d3.tsvFormat(data.slice(0, 24)));

        return Promise.resolve();
      }
    },
  },
  async mounted() {
    const __VM = this;
    await __VM.init();

    let resizeTimer;
    d3.select(window).on("resize", async () => {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(async () => {
        await __VM.init();
      }, 250);
    });
  },
  watch: {},
};
</script>

<style>
svg {
  font: 10px sans-serif;
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
}

.axis .yLabel {
  font-weight: bolder;
  font-size: 1rem;
}

pre {
  width: 100%;
  height: 300px;
  tab-size: 15;
  font-size: 10px;
}
</style>
