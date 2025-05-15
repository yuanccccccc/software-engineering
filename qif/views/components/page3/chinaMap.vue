<template>
  <div class="chinaMap"></div>
</template>

<script>
import "@/lib/china.js"
import axios from 'axios'

export default {
  name: 'ChinaMapProvinceTrend',
  data() {
    return {
      myChart: null
    }
  },
  methods: {
    async setMap() {
      const response1 = await axios.get("http://localhost:5000/api/province_total")
      const provinceSeries = response1.data
      const data = provinceSeries.map(item => ({ name: item.name, value: item.value }))

      const response2 = await axios.get("http://localhost:5000/api/province_trend")
      const topTrend = response2.data.slice(0, 6) // 限制为最多6条

      const geoCoordMap = {
        '北京市': [116.40, 39.90], '天津市': [117.20, 39.13], '上海市': [121.47, 31.23],
        '重庆市': [106.55, 29.57], '河北省': [114.52, 38.05], '山西省': [112.55, 37.87],
        '辽宁省': [123.43, 41.80], '吉林省': [125.32, 43.90], '黑龙江省': [126.63, 45.75],
        '江苏省': [118.78, 32.04], '浙江省': [120.15, 30.28], '安徽省': [117.28, 31.86],
        '福建省': [119.30, 26.08], '江西省': [115.89, 28.68], '山东省': [117.00, 36.65],
        '河南省': [113.65, 34.76], '湖北省': [114.30, 30.60], '湖南省': [112.93, 28.23],
        '广东省': [113.27, 23.13], '海南省': [110.35, 20.02], '四川省': [104.06, 30.67],
        '贵州省': [106.71, 26.57], '云南省': [102.71, 25.04], '陕西省': [108.95, 34.27],
        '甘肃省': [103.82, 36.05], '青海省': [101.78, 36.62], '台湾省': [121.51, 25.05],
        '内蒙古自治区': [111.65, 40.82], '广西壮族自治区': [108.32, 22.82],
        '西藏自治区': [91.11, 29.97], '宁夏回族自治区': [106.27, 38.47],
        '新疆维吾尔自治区': [87.62, 43.82], '香港特别行政区': [114.17, 22.32],
        '澳门特别行政区': [113.55, 22.20]
      }

      const convertData = data => data.map(item => {
        const coord = geoCoordMap[item.name] || null
        return coord ? { name: item.name, value: coord.concat(item.value) } : null
      }).filter(Boolean)

      const option = {
        title: topTrend.map((item, idx) => ({
          text: item.province,
          top: idx % 2 === 0 ? '4.8%' : '11.5%',
          left: `${7.5 + Math.floor(idx / 2) * 30}%`,
          textStyle: { color: '#fff', fontSize: 12, fontWeight: 'normal' }
        })),
        grid: topTrend.map((_, idx) => ({
          top: idx % 2 === 0 ? '3%' : '10%',
          left: `${17.5 + Math.floor(idx / 2) * 30}%`,
          right: `${67.5 - Math.floor(idx / 2) * 30}%`,
          height: '5%'
        })),
        xAxis: topTrend.map((item, idx) => ({
          gridIndex: idx,
          axisLabel: { show: false },
          axisTick: { show: false },
          axisLine: { lineStyle: { color: '#999' } },
          inverse: true,
          boundaryGap: false,
          data: item.dates
        })),
        yAxis: topTrend.map((_, idx) => ({
          gridIndex: idx,
          type: 'value',
          axisLabel: { show: false },
          position: 'right',
          axisLine: { show: false },
          axisTick: { show: false },
          splitLine: { show: false }
        })),
        geo: {
          map: 'china',
          roam: false,
          label: { show: false },
          itemStyle: {
            areaColor: '#2043AA',
            borderColor: '#111'
          }
        },
        series: [
          {
            name: 'pm2.5',
            type: 'effectScatter',
            coordinateSystem: 'geo',
            data: convertData(data.sort((a, b) => b.value - a.value).slice(0, 31)),
            symbolSize: val => val[2] / 150,
            showEffectOn: 'render',
            emphasis: { scale: true },
            label: { formatter: '{b}', position: 'right', show: false },
            itemStyle: {
              color: params => {
                const colorList = ['#FFA200', '#0006FF', '#D6FC01', '#00D8FF', '#FF00CC', '#FF1200']
                return colorList[params.dataIndex % colorList.length]
              },
              shadowBlur: 10
            },
            zlevel: 1
          },
          ...topTrend.map((item, idx) => ({
            type: 'line',
            xAxisIndex: idx,
            yAxisIndex: idx,
            smooth: true,
            lineStyle: {
              color: ['#A11780', '#C46714', '#B5AE1C', '#A50F47', '#10B6A5', '#0953B0'][idx],
              width: 1
            },
            areaStyle: {
              color: {
                type: 'linear',
                x: 0, y: 0, x2: 0, y2: 1,
                colorStops: [
                  { offset: 0, color: ['#A11780', '#C46714', '#B5AE1C', '#A50F47', '#10B6A5', '#0953B0'][idx] },
                  { offset: 1, color: 'rgba(0,0,0,0)' }
                ]
              }
            },
            data: item.counts.map((val, i) => ({
              value: val,
              symbol: i === 0 ? 'circle' : 'none',
              symbolSize: 5,
              itemStyle: {
                color: '#293880',
                borderColor: ['#A11780', '#C46714', '#B5AE1C', '#A50F47', '#10B6A5', '#0953B0'][idx],
                borderWidth: 1
              }
            }))
          }))
        ]
      }

      if (!this.myChart) this.myChart = this.$echarts(this.$el)
      this.myChart.clear()
      this.myChart.resize()
      this.myChart.setOption(option)
    }
  },
  mounted() {
    this.setMap()
  }
}
</script>

<style lang="less" scoped>
.chinaMap {
  height: 100%;
}
</style>
