<template>
  <v-menu
    left
    offset-x
    open-on-hover
    lazy
  >
    <base-chart-horizontal-bar
      slot="activator"
      v-bind:styles="{
        height: `${height}px`,
        width: `${width}px`,
        'margin-bottom': '-10px',
        'margin-left': 'auto',
        'margin-right': 'auto',
      }"
      v-bind:chartdata="chartdata"
      v-bind:options="options"
    />

    <v-list
      dense
    >
      <v-subheader>{{ titlePopover }}</v-subheader>

      <v-list-tile
        v-for="(item, index) in chartdata.datasets"
        v-bind:key="index"
      >
        <v-list-tile-title
          v-bind:style="{ color: item.backgroundColor }"
        >
          {{ item.label }}
        </v-list-tile-title>
        <v-list-tile-title>
          {{ item.data[0] }}
        </v-list-tile-title>
      </v-list-tile>
    </v-list>
  </v-menu>
</template>

<script>
import BaseChartHorizontalBar from './charts/base-chart-horizontal-bar';

export default {
  name: 'BaseProgressBar',
  components: { BaseChartHorizontalBar },
  props: {
    titlePopover: {
      required: true,
      type: String,
    },
    datasets: {
      required: true,
      type: Array,
    },
  },
  data() {
    return {
      height: 28,
      width: 200,
      chartdata: {
        datasets: this.datasets,
      },
      options: {
        tooltips: {
          enabled: false,
        },
        hover: {
          mode: null,
        },
        responsive: true,
        maintainAspectRatio: false,
        legend: false,
        animation: {
          duration: 0,
        },
        scales: {
          xAxes: [{
            stacked: true,
            gridLines: {
              display: false,
              drawBorder: false,
            },
            ticks: {
              // all bars same width
              stepSize: 1,
              display: false,
            },
          }],
          yAxes: [{
            stacked: true,
            gridLines: {
              display: false,
              drawBorder: false,
            },
            barThickness: 15,
            ticks: {
              display: false,
            },
          }],
        },
      },
    };
  },
};
</script>
