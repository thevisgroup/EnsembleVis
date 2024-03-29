<template>
  <div>
    <div id="parallelCoordinates"></div>
    <b-table
      id="inputTable"
      striped
      hover
      fixed
      sticky-header
      :items="options.show_selected_rows_only ? options.table.selectedRows : options.table.initData"
      :fields="headers"
      :sort-by.sync="sortBy"
      sort-desc.sync="false"
      responsive="sm"
    >
      <template #cell(Index)="row">
        <b-button
          size="xs"
          :variant="options.simulation_selected === row.item.Index ? 'primary' : 'secondary'"
          @click="clickHeader(row.item)"
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
            :value="getBarValue(data.value / input_meta[2][data.field.key], true)"
            variant="empty"
          >
          </b-progress-bar>
          <b-progress-bar
            :value="getBarValue(data.value / input_meta[2][data.field.key], false)"
            :style="getBarVariant(data.value / input_meta[2][data.field.key])"
            :striped="data.field.key === sortBy"
            :animated="data.field.key === sortBy"
          >
          </b-progress-bar>
        </b-progress>
        <b-tooltip
          :target="`b-progress-${data.item.Index + data.field.key}`"
          placement="rightbottom"
        >
          {{ data.value }}
        </b-tooltip>
      </template>
    </b-table>
  </div>
</template>

<script>
import * as d3 from "d3";
import { mapState, mapGetters } from "vuex";

const tableColor = d3.scaleSequential(d3.interpolatePRGn);

export default {
  name: "ParallelCoordinates",
  computed: {
    ...mapState(["options"]),
    ...mapGetters("options", ["isRowSelected"]),
  },
  data() {
    return {
      rowsToDisplay: 160,
      headers: [],
      input_meta: null,
      sortBy: "Index",
      x: null,
      y: null,
    };
  },
  methods: {
    async init() {
      const __VM = this;

      d3.selectAll("#parallelCoordinates > svg").remove();

      __VM.options.table.initData = await d3.csv("/assets/posterior_parameters.csv", d3.autoType);

      if (__VM.options.table.selectedRows.length === 0) {
        __VM.options.table.selectedRows = __VM.options.table.initData;
      }

      __VM.input_meta = await d3.csv("/assets/posterior_parameters_meta.csv", d3.autoType);

      const margin = { top: 30, right: -100, bottom: 10, left: -100 };
      const width = window.innerWidth - margin.left - margin.right;
      const height = window.innerHeight / 1.5 - margin.top - margin.bottom;

      __VM.x = d3.scalePoint().range([0, width]).padding(1);
      __VM.y = {};

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
      __VM.x.domain(
        (__VM.options.pcp.dimensions = __VM.options.table.initData.columns.filter((d) => {
          return (
            d !== "Index" &&
            (__VM.y[d] = d3
              .scaleLinear()
              .domain(
                d3.extent(__VM.options.table.initData, function (p) {
                  return +p[d];
                })
              )
              .range([height, 0]))
          );
        }))
      );

      __VM.headers = __VM.options.table.initData.columns.map((d) => {
        const res = { key: d, sortable: true };

        if (d === "Index") {
          res.variant = "secondary";
          res.stickyColumn = true;
        }
        return res;
      });

      let colors = {};
      __VM.options.table.initData.columns.map((d) => {
        colors[d] = d3
          .scaleSequential()
          .domain(
            d3.extent(__VM.options.table.initData, function (d) {
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
        .data(__VM.options.table.initData)
        .enter()
        .append("path")
        .attr("d", path);

      // Add blue foreground lines for focus.
      foreground = svg
        .append("g")
        .attr("class", "foreground")
        .selectAll("path")
        .data(__VM.options.table.selectedRows)
        .enter()
        .append("path")
        .attr("d", path);

      // Add a group element for each dimension.
      const g = svg
        .selectAll(".dimension")
        .data(__VM.options.pcp.dimensions)
        .enter()
        .append("g")
        .attr("class", "dimension")
        .attr("transform", (d) => "translate(" + __VM.x(d) + ")");

      // Add an axis and title.
      g.append("g")
        .attr("class", "axis")
        .each(function (d) {
          d3.select(this).call(axis.scale(__VM.y[d]));
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
            (__VM.y[d].brush = d3
              .brushY()
              .extent([
                [-10, 0],
                [10, height],
              ])
              .on("brush", brushStart)
              .on("end", brushEnd))
          );
        })
        .selectAll("rect")
        .attr("x", -8)
        .attr("width", 16);

      // Returns the path for a given data point.
      function path(d) {
        const res = d3.line()(
          __VM.options.pcp.dimensions.map(function (p) {
            return [__VM.x(p), __VM.y[p](d[p])];
          })
        );
        return res;
      }

      // __VM.options.table.selectedRows = __VM.options.table.initData;

      let display = [];
      let actives = [];
      // Handles a brush event, toggling the display of foreground lines.
      function brush() {
        actives = [];
        svg
          .selectAll(".brush")
          .filter(function (d) {
            __VM.y[d].brushSelectionValue = d3.brushSelection(this);
            return d3.brushSelection(this);
          })
          .each(function (d) {
            // Get extents of brush along each active selection axis (the Y axes)
            actives.push({
              dimension: d,
              extent: d3.brushSelection(this).map(__VM.y[d].invert),
            });
          });

        let local_selected = [];
        // Update foreground to only display selected values
        foreground.style("display", function (d) {
          return actives.every(function (active) {
            let result =
              active.extent[1] <= d[active.dimension] && d[active.dimension] <= active.extent[0];
            if (result || __VM.options.simulation_selected === d.Index) {
              local_selected.push(d);
            }
            return result;
          })
            ? null
            : "none";
        });

        display = [];
        local_selected.forEach((l) => {
          if (local_selected.filter((s) => s.Index === l.Index).length === actives.length) {
            display.push(l);
          }
        });
      }

      function brushStart() {
        brush();
      }

      function brushEnd() {
        brush();

        // refresh table on brushEnd
        actives.length > 0
          ? (__VM.options.table.selectedRows = [...new Set(display)])
          : (__VM.options.table.selectedRows = __VM.options.table.initData);

        // trigger PCA redraw
        __VM.options.pca.count++;
      }

      __VM.clickHeader(__VM.options.table.initData[0]);
    },
    // redraw() {
    //   const __VM = this;

    //   d3.select("#parallelCoordinates > svg > g > g.foreground").remove();

    //   d3.select("#parallelCoordinates > svg > g")
    //     .append("g")
    //     .attr("class", "foreground")
    //     .selectAll("path")
    //     .data(__VM.options.table.selectedRows)
    //     .enter()
    //     .append("path")
    //     .attr("d", path);

    //   // let pc1 = d3
    //   //   .select("#parallelCoordinates > svg > g > g.foreground")
    //   //   .selectAll("path")
    //   //   .data(__VM.options.table.selectedRows);

    //   // pc1.exit().remove();

    //   // pc1.enter().append("path").attr("d", path);

    //   // Returns the path for a given data point.
    //   function path(d) {
    //     const res = d3.line()(
    //       __VM.options.pcp.dimensions.map(function (p) {
    //         return [__VM.x(p), __VM.y[p](d[p])];
    //       })
    //     );
    //     return res;
    //   }
    // },
    getBarVariant(data) {
      return `background-color: ${tableColor(data)};`;
    },

    getIndexVariant(index) {
      const __VM = this;

      if (__VM.options.simulation_selected === index) {
        return "primary";
      }

      if (__VM.isRowSelected(index)) {
        return "danger";
      } else {
        return "secondary";
      }
    },

    getBarValue(data, isOnTheLeft) {
      if (data > 0.5) {
        return isOnTheLeft ? 0.5 : data - 0.5;
      } else if (data <= 0.5) {
        return isOnTheLeft ? data : 0.5 - data;
      }
    },
    getTableHeaderClass(column) {
      if (column === this.sortBy) {
        return "text-danger";
      } else {
        return "text";
      }
    },
    clickHeader(item) {
      const __VM = this;

      __VM.options.simulation_selected = item.Index;

      let columns = Object.create(item);
      delete columns.Index;

      let sortedKeys = Object.keys(
        Object.fromEntries(
          Object.entries(item).sort(([k1, v1], [k2, v2]) => {
            return v1 / __VM.input_meta[2][k1] - v2 / __VM.input_meta[2][k2];
          })
        )
      );

      let newHeaders = sortedKeys.map((k) => {
        return {
          key: k,
          sortable: true,
        };
      });

      newHeaders.unshift({
        key: "Index",
        sortable: true,
        stickyColumn: true,
        variant: "secondary",
        tdClass: (v) => __VM.getTableIndexBackground(v),
      });

      __VM.headers = newHeaders;
    },
    getTableIndexBackground(v) {
      if (this.isRowSelected(v)) {
        return "table-danger";
      } else {
        return "table-secondary";
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
  watch: {
    "options.pcp.count": {
      handler: function () {
        this.init();
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

/* empty bar hack */
.bg-empty {
  background-color: #e9ecef;
}

/* xs button for table */
.btn-xs {
  padding: 0.1rem 0.3rem;
  font-size: 0.6rem;
}

/* special table padding */
#inputTable td {
  padding: 0rem 0.3rem !important;
}
</style>
