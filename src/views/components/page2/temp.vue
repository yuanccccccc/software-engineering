<template>
  <div ref="chart" style="width: 100%; height: 100%"></div>
</template>

<script>
import * as echarts from 'echarts'
//import 'echarts/theme/walden'
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
  mounted() {
    axios.get(this.apiUrl).then(res => {
      const { nodes, links } = res.data

      const chart = echarts.init(this.$refs.chart, 'walden')
      chart.setOption({
        //backgroundColor: '#151456',
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
            label: {
              show: false   // ✅ 不显示节点名称
            },
            itemStyle: {
              borderColor: '#6EDDF1',  // ✅ 节点边框颜色
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

      window.addEventListener('resize', () => chart.resize())
    })
  }
}
</script>

<style lang="less" scoped>
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

.chart-container {
  width: 100%;
  height: 100%;
}
</style>
