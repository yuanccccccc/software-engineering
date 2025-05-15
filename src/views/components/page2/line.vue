<template>
  <div class="chart-wrapper">
    <!-- 所有筛选字段 -->
    <div class="filters">
      <div v-for="(options, key) in filterOptions" :key="key" class="filter-item">
        <label>{{ key }}：</label>
        <select v-model="filters[key]" @change="onFilterChange">
          <option value="">全部</option>
          <option v-for="opt in options" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>

      <!-- 展示数据单选，统一为下拉框 -->
      <div class="filter-item">
        <label>展示数据：</label>
        <select v-model="selectedMetric" @change="fetchData">
          <option v-for="metric in metrics" :key="metric" :value="metric">
            {{ metric.replace(/\(.*?\)/, '') }}
          </option>
        </select>
      </div>
    </div>

    <!-- 图表区域 -->
    <div ref="chart" class="chart-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export default {
  name: 'WaterQualityChart',
  data() {
    return {
      chart: null,
      filters: {
        省份: '',
        流域: '',
        断面名称: '',
        年份: '',
        月份: '',
        日期: ''
      },
      filterOptions: {},
      chartData: [],
      metrics: [
        '溶解氧(mg/L)', '电导率(μS/cm)', 'pH(无量纲)', '氨氮(mg/L)',
        '总磷(mg/L)', '总氮(mg/L)', '水温(℃)', '高锰酸盐指数(mg/L)', '浊度(NTU)'
      ],
      selectedMetric: '水温(℃)' // 默认选中温度
    }
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart, 'walden')
    this.fetchFilterOptions()
    this.fetchData()
  },
  methods: {
    onFilterChange() {
      this.fetchFilterOptions()
      this.fetchData()
    },
    selectMetric(metric) {
      this.selectedMetric = metric
      this.fetchData()
    },
    async fetchFilterOptions() {
      try {
        const res = await axios.get(`${API_BASE}/filter_options`, {
          params: this.filters
        })
        this.filterOptions = res.data
        for (const key of Object.keys(res.data)) {
          if (!(key in this.filters)) {
            this.$set(this.filters, key, '')
          }
        }
      } catch (err) {
        console.error('获取筛选项失败：', err)
      }
    },
    async fetchData() {
      try {
        const res = await axios.get(`${API_BASE}/water_quality`, {
          params: {
            ...this.filters,
            metric: this.selectedMetric  // ✅ 向后端传递所选指标字段
          }
        })
        this.chartData = res.data
        this.updateChart()
      } catch (err) {
        console.error('获取图表数据失败：', err)
      }
    },
    updateChart() {
      if (!this.chart || !this.selectedMetric) return

      const dates = this.chartData.map(d => d['日期'] || '')
      const cleanName = this.selectedMetric.replace(/\(.*?\)/, '')
      const values = this.chartData.map(d => parseFloat(d[this.selectedMetric]) || 0)

      const option = {
        // title: {
        //   text: '水质变化趋势',
        //   textStyle: { color: '#fff' }
        // },
        tooltip: { trigger: 'axis' },
        // legend: {
        //   data: [cleanName],
        //   textStyle: { color: '#fff' }
        // },
        xAxis: {
          type: 'category',
          data: dates,
          axisLabel: { color: '#fff' }
        },
        yAxis: {
          type: 'value',
          name: cleanName,
          axisLabel: { color: '#fff' },
          nameTextStyle: { color: '#fff' },
          axisLine: { lineStyle: { color: '#ccc' } }
        },
        series: [
          {
            name: cleanName,
            type: 'line',
            data: values
          }
        ]
      }

      this.chart.setOption(option)
    }
  }
}
</script>

<style scoped>
.chart-wrapper {
  width: 100%;
  height: 100%;
  background: #151456;
  padding: 10px;
overflow: hidden; /* ✅ 禁止滚动条 */
}
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 5px;
}
.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 60px;
  margin-right: 10px;
}

.filter-item label {
  color: #00ccff;
  font-weight: bold;
  margin-bottom: 4px;
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

.metric-list {
  list-style: none;
  padding: 0;
  margin: 0;
  background: #1f1f5e;
  border-radius: 6px;
}
.metric-list li {
  padding: 4px 10px;
  cursor: pointer;
  color: white;
}
.metric-list li.selected {
  background-color: #3d6eff;
  font-weight: bold;
  border-radius: 4px;
}
.chart-container {
  width: 100%;
  height: 380px;
  overflow: hidden; /* ✅ 禁止滚动条 */
}
</style>
