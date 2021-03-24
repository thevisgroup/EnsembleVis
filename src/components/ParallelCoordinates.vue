<template>
  <div>
    <div id="parallelCoordinates"></div>
    <b-table
      striped
      hover
      sticky-header
      :items="tableData"
      :fields="headers"
      :sort-by.sync="sortBy"
      sort-desc.sync="false"
      responsive="sm"
    >
      <template #cell(Index)="row">
        <b-button
          size="sm"
          :variant="options.simulation_selected === row.item.Index ? 'primary' : 'secondary'"
          @click="options.simulation_selected = row.item.Index"
          class="mr-2"
        >
          {{ row.item.Index }}
        </b-button>
      </template>

      <template #head()="data">
        <span :class="getTableHeaderClass(data.field.key)">{{ data.field.key }}</span>
      </template>

      <template #cell()="data">
        <div v-if="options.table.showAvgLine" class="bar-step" style="left: 50%">
          <div class="label-line"></div>
        </div>
        <b-progress max="1" :id="`b-progress-${data.item.Index + data.field.key}`">
          <b-progress-bar
            :value="data.value / input_meta[2][data.field.key]"
            :variant="getBarVariant(data.value / input_meta[2][data.field.key])"
            :striped="data.field.key === sortBy"
            :animated="data.field.key === sortBy"
          >
          </b-progress-bar>
        </b-progress>
        <b-tooltip :target="`b-progress-${data.item.Index + data.field.key}`">
          {{ data.value }}
        </b-tooltip>
      </template>
    </b-table>
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapState } from "vuex";

export default {
  name: "ParallelCoordinates",
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
      input_meta: null,
      sortBy: "Index",
    };
  },
  methods: {
    async init() {
      const __VM = this;

      d3.selectAll("#parallelCoordinates > svg").remove();

      __VM.data = await d3.csv("/assets/posterior_parameters.csv", d3.autoType);

      __VM.input_meta = await d3.csv("/assets/posterior_parameters_meta.csv", d3.autoType);

      const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight / 1.5 - margin.top - margin.bottom;

      const x = d3.scalePoint().range([0, width]).padding(1);
      const y = {};

      const colorScheme = d3.interpolateTurbo;
      const axis = d3.axisLeft();

      let background, foreground;

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
        (__VM.dimensions = __VM.data.columns.filter((d) => {
          return (
            d !== "Index" &&
            (y[d] = d3
              .scaleLinear()
              .domain(
                d3.extent(__VM.data, function (p) {
                  return +p[d];
                })
              )
              .range([height, 0]))
          );
        }))
      );

      __VM.headers = __VM.data.columns.map((d) => {
        const res = { key: d, sortable: true };

        if (d === "Index") {
          res.variant = "secondary";
          res.stickyColumn = true;
        }
        return res;
      });

      let colors = {};
      __VM.data.columns.map((d) => {
        colors[d] = d3
          .scaleSequential()
          .domain(
            d3.extent(__VM.data, function (d) {
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
        .data(__VM.data)
        .enter()
        .append("path")
        .attr("d", path);

      // Add blue foreground lines for focus.
      foreground = svg
        .append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(__VM.data)
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

      __VM.tableData = __VM.data.slice(0, __VM.rowsToDisplay);

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
          ? (__VM.tableData = [...new Set(display)].slice(0, __VM.rowsToDisplay))
          : (__VM.tableData = __VM.data.slice(0, __VM.rowsToDisplay));

        return Promise.resolve();
      }
    },

    getBarVariant(data) {
      if (data > 0.75) {
        return "success";
      } else if (data >= 0.5) {
        return "primary";
      } else if (data >= 0.25) {
        return "warning";
      } else {
        return "danger";
      }
    },
    getTableHeaderClass(column) {
      if (column === this.sortBy) {
        return "text-danger";
      } else {
        return "text";
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

.bar-step {
  position: relative;
}

.label-line {
  position: absolute;
  background: #000;
  height: 1rem;
  width: 2px;
  margin-left: -1px;
}
</style>
