<template>
  <div ref="plot" class="chart-container" style="width: 100%; height: 80%;"></div>
</template>

<script>
import Plotly from 'plotly.js-dist-min';
import axios from 'axios';

export default {
  name: 'FishViolinPlot',
  data() {
    return {
      rawData: []
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get('http://localhost:5000/api/fish_data');
        this.rawData = res.data;
        this.renderChart();
      } catch (err) {
        console.error("获取数据失败", err);
      }
    },
    renderChart() {
      if (!this.rawData.length) return;

      const speciesMap = {};
      this.rawData.forEach(item => {
        const species = item["Species"];
        if (!speciesMap[species]) speciesMap[species] = [];
        speciesMap[species].push(item["Weight(g)"]);
      });

      const colorList = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b'];

      const traces = Object.entries(speciesMap).map(([species, weights], index) => {
        const color = colorList[index % colorList.length];
        return {
          type: 'violin',
          y: weights,
          name: species,
          box: { visible: true },
          meanline: { visible: true },
          line: { color: color },
          fillcolor: color + '93', // 添加透明度
          points: 'all',
          jitter: 0.3,
          scalemode: 'count',
          marker: { size: 4, color: color },
          hovertemplate: `鱼类：${species}<br>体重：%{y} g<extra></extra>`
        };
      });

      const layout = {
        title: '不同鱼类的体重分布小提琴图',
        paper_bgcolor: '#03044A',
        plot_bgcolor: '#03044A',
        font: { color: '#fff' },
        yaxis: {
          title: '体重 (g)',
          zeroline: false
        },
        xaxis: {
          title: '鱼类种类'
        },
        hovermode: 'closest'
      };

      Plotly.newPlot(this.$refs.plot, traces, layout, { responsive: true });
    }
  }
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 60vh;
  min-height: 400px;
}
</style>
