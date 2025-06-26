<template>
  <div class="chart-wrapper">
    <!-- ✅ 筛选字段 + 下载按钮 -->
    <div class="filters">
      <div v-for="(options, key) in filterOptions" :key="key" class="filter-item">
        <label>{{ key }}：</label>
        <select v-model="filters[key]" @change="onFilterChange">
          <option value="">全部</option>
          <option v-for="opt in options" :key="opt" :value="opt">{{ opt }}</option>
        </select>
      </div>

      <div class="filter-item">
        <label>展示数据：</label>
        <select v-model="selectedMetric" @change="fetchData">
          <option v-for="metric in metrics" :key="metric" :value="metric">
            {{ metric.replace(/\(.*?\)/, '') }}
          </option>
        </select>
      </div>

      <!-- ✅ 下载按钮 -->
      <div class="filter-item download-item">
        <label style="visibility: hidden;">下载</label>
        <button class="download-btn" @click="downloadChart('water_quality_chart.png')">下载图表</button>
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
      selectedMetric: '水温(℃)'
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
            metric: this.selectedMetric
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
        tooltip: { trigger: 'axis' },
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
    },
    // ✅ 下载图表为 PNG
    downloadChart(filename = 'chart.png') {
      if (!this.chart) return
      const url = this.chart.getDataURL({
        type: 'png',
        backgroundColor: '#fff',
        pixelRatio: 2
      })
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      link.click()
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
  overflow: hidden;
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

.download-item {
  justify-content: flex-end;
}

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

.chart-container {
  width: 100%;
  height: 380px;
  overflow: hidden;
}
</style>
