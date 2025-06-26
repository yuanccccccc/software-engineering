<template>
  <div class="leftBar">
    <h3 class="chart-title">水温/PH值与省份的关系</h3>

    <!-- ✅ 工具栏 -->
    <div class="toolbar">
      <div>
        <label style="color: white; font-size: 12px;">筛选省份：</label>
        <select v-model="selectedProvince" @change="fetchData">
          <option value="">全部</option>
          <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
      <button class="download-btn" @click="downloadChart('pht_chart.png')">下载图表</button>
    </div>

    <div ref="chart" class="chart-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import '@/assets/walden.js'
import axios from 'axios'

export default {
  name: 'phtChart',
  data() {
    return {
      chart: null,
      selectedProvince: '',
      provinces: []
    }
  },
  methods: {
    async fetchData() {
      const url = this.selectedProvince
        ? `http://localhost:5000/api/pht?province=${encodeURIComponent(this.selectedProvince)}`
        : 'http://localhost:5000/api/pht'

      const res = await axios.get(url)
      const { points, avg_temp, avg_ph, provinces } = res.data
      this.provinces = provinces

      const option = {
        grid: [
          { top: '15%', height: '40%' },
          { bottom: '5%', top: '60%', height: '35%' }
        ],
        tooltip: { trigger: 'item' },
        xAxis: { name: '温度 (℃)', type: 'value', gridIndex: 0, min: 0, max: 32 },
        yAxis: { name: 'pH 值', type: 'value', gridIndex: 0, min: 6, max: 10 },
        series: [
          {
            type: 'scatter',
            name: '温度 vs pH',
            xAxisIndex: 0,
            yAxisIndex: 0,
            data: points,
            symbolSize: 8,
            itemStyle: { color: '#3398DB' }
          },
          {
            type: 'gauge',
            center: ['30%', '90%'],
            radius: '40%',
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 40,
            splitNumber: 4,
            axisLine: { lineStyle: { color: [[1, '#FF9F7F']], width: 6 } },
            pointer: { show: true },
            title: { offsetCenter: [0, '-20%'], fontSize: 10, color: '#fff' },
            detail: { formatter: '{value} ℃', fontSize: 12, color: '#fff' },
            data: [{ value: avg_temp, name: '平均温度' }]
          },
          {
            type: 'gauge',
            center: ['75%', '90%'],
            radius: '40%',
            startAngle: 180,
            endAngle: 0,
            min: 0,
            max: 14,
            splitNumber: 7,
            axisLine: { lineStyle: { color: [[1, '#37A2DA']], width: 6 } },
            pointer: { show: true },
            title: { offsetCenter: [0, '-20%'], fontSize: 10, color: '#fff' },
            detail: { formatter: 'pH {value}', fontSize: 12, color: '#fff' },
            data: [{ value: avg_ph, name: '平均pH' }]
          }
        ]
      }

      if (!this.chart) this.chart = echarts.init(this.$refs.chart, 'walden')
      this.chart.setOption(option, true)
    },

    // ✅ 下载图表为 PNG
    downloadChart(filename = 'chart.png') {
      if (!this.chart) return;
      const url = this.chart.getDataURL({
        type: 'png',
        backgroundColor: '#fff',
        pixelRatio: 2
      });
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      link.click();
    }
  },
  mounted() {
    this.fetchData()
  }
}
</script>

<style scoped>
.leftBar {
  height: 100%;
  width: 100%;
  background: #151456;
  border: 1px solid #0D2451;
  padding: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  border-radius: 6px;
  overflow: hidden;
}

.chart-title {
  color: #ffffff;
  font-size: 14px;
  font-weight: bold;
  margin-bottom: 10px;
}

.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

/* ✅ 下载按钮样式 */
.download-btn {
  background: rgba(92, 169, 230, 0.6);
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.3s ease;
}
.download-btn:hover {
  background: rgba(92, 169, 230, 0.9);
}

.chart-container {
  width: 100%;
  height: calc(100% - 80px); /* 留出标题和工具栏空间 */
  margin-top: 5px;
}

select {
  background: linear-gradient(135deg, #0d1a33, #102040);
  border: 1px solid #00ccff;
  border-radius: 6px;
  padding: 6px 10px;
  color: #63ddff;
  font-size: 8px;
  outline: none;
  box-shadow: 0 0 8px rgba(0, 204, 255, 0.3);
  transition: box-shadow 0.3s ease;
}

select:hover {
  box-shadow: 0 0 12px rgba(0, 204, 255, 0.6);
  border-color: #33ccff;
}
</style>
