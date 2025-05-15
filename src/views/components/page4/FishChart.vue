<template>
  <div ref="chart" class="chart-container" style="width: 100%; height: 80%;"></div>
</template>

<script>
import * as echarts from 'echarts';
import axios from 'axios';

export default {
  name: 'FishChart',
  data() {
    return {
      chart: null,
      rawData: []
    };
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart);
    this.fetchData();
    this.resizeHandler = () => this.chart && this.chart.resize();
    window.addEventListener('resize', this.resizeHandler);
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.resizeHandler);
    if (this.chart) this.chart.dispose();
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get('http://localhost:5000/api/fish_data');
        this.rawData = res.data;
        this.renderChart();
      } catch (error) {
        console.error('请求鱼类数据失败', error);
      }
    },
    renderChart() {
      if (!this.rawData.length) return;

      // 以鱼类分类，每类为一个 series
      const speciesMap = {};
      this.rawData.forEach(item => {
        const species = item["Species"];
        if (!speciesMap[species]) {
          speciesMap[species] = [];
        }
        speciesMap[species].push({
          value: [item["Length1(cm)"], item["Weight(g)"]],
          name: species,
          info: item
        });
      });

      // 构建每个鱼类对应一个系列
      const series = Object.entries(speciesMap).map(([species, data]) => ({
        name: species,
        type: 'scatter',
        data,
        symbolSize: 10,
        emphasis: {
          focus: 'series'
        }
      }));

      const option = {
        title: {
          text: '鱼类体重 vs 长度1 散点图',
          textStyle: { color: '#fff' }
        },
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            const data = params.data.info;
            return `
              <b>鱼类：</b>${data.Species}<br/>
              <b>体重：</b>${data["Weight(g)"]} g<br/>
              <b>长度：</b>${data["Length1(cm)"]} cm<br/>
              <b>高度：</b>${data["Height(cm)"]} cm<br/>
              <b>宽度：</b>${data["Width(cm)"]} cm
            `;
          }
        },
        legend: {
          type: 'scroll',
          bottom: 0,
          textStyle: { color: '#fff' }
        },
        xAxis: {
          type: 'value',
          name: 'Length1 (cm)',
          axisLine: { lineStyle: { color: '#fff' } },
          axisLabel: { color: '#fff' }
        },
        yAxis: {
          type: 'value',
          name: 'Weight (g)',
          axisLine: { lineStyle: { color: '#fff' } },
          axisLabel: { color: '#fff' }
        },
        series,
        backgroundColor: '#03044A'
      };

      this.chart.setOption(option);
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
