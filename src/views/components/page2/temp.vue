<template>
  <div class="chart-wrapper">
    <!-- ✅ 工具栏：按钮单独占一行 -->
    <div class="chart-toolbar">
      <button @click="downloadChart('水质关系图.png')" class="download-btn">
        下载图表
      </button>
    </div>

    <!-- ✅ 图表主体 -->
    <div ref="chart" class="chart-container"></div>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import '@/assets/walden.js'
import axios from 'axios'

export default {
  name: 'MyWaterChart',
  props: {
    apiUrl: {
      type: String,
      default: 'http://localhost:5000/api/sankey'
    }
  },
  data() {
    return {
      chart: null
    }
  },
  mounted() {
    axios.get(this.apiUrl).then(res => {
      const { nodes, links } = res.data

      this.chart = echarts.init(this.$refs.chart, 'walden')
      this.chart.setOption({
        title: {
          text: '水质类别与流域/省份间的关系',
          left: 'left',
          top: '5%',
          textStyle: {
            color: '#FFFFFF',
            fontSize: 12,
            fontWeight: 'bold'
          }
        },
        tooltip: {
          trigger: 'item',
          backgroundColor: '#1F1E4E',
          textStyle: {
            color: '#8CBCCD',
            fontSize: 12
          },
          formatter: function (params) {
            if (params.dataType === 'edge') {
              return `${params.data.source} → ${params.data.target}<br/>数量：${params.data.value}`
            } else {
              return params.name
            }
          }
        },
        series: [
          {
            type: 'sankey',
            data: nodes,
            links: links,
            layout: 'none',
            nodeAlign: 'center',
            left: '10%',
            right: '10%',
            top: '15%',
            nodeWidth: 20,
            nodeGap: 2,
            draggable: false,
            emphasis: { focus: 'adjacency' },
            label: { show: false },
            itemStyle: {
              borderColor: '#6EDDF1',
              borderWidth: 1,
              shadowColor: '#0D2451',
              shadowBlur: 8
            },
            lineStyle: {
              color: 'source',
              opacity: 0.6,
              curveness: 0.5
            }
          }
        ]
      })

      window.addEventListener('resize', () => this.chart.resize())
    })
  },
  methods: {
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
  }
}
</script>

<style lang="less" scoped>
.chart-wrapper {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
  background: #151456;
  border: 1px solid #0D2451;
  border-radius: 6px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

/* ✅ 工具栏样式 */
.chart-toolbar {
  height: 36px;
  display: flex;
  justify-content: flex-end;
  align-items: center;
  padding: 0 10px;
  background: transparent;
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

/* ✅ 图表容器 */
.chart-container {
  flex: 1;
  width: 100%;
}
</style>
