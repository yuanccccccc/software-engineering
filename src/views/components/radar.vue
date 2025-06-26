<template>
  <div class="chart"></div>
</template>

<style lang="less" scoped>
.chart {
  height: 100%;
}
</style>

<script>
export default {
  name: 'Radar',
  props: {
    data: Object
  },
  data() {
    return {
      myChart: null
    }
  },
  methods: {
    setChart() {
      console.log("[Radar] 渲染图表中 ID:", this.id);
      console.log("[Radar] 接收到的数据：", this.data);

      const seriesData = this.data.data.map(item => ({
        value: item.value,
        name: item.name,
        symbol: 'none',
        symbolSize: 5,
        itemStyle: { color: item.color },
        lineStyle: { color: item.color, width: 1 },
        emphasis: {
          lineStyle: { width: 2 }
        }
      }));

      const option = {
        tooltip: {
          trigger: 'item',
          axisPointer: {
            type: 'shadow'
          }
        },
        title: {
          text: this.data.title,
          top: "5%",
          left: 'center',
          textStyle: {
            color: '#fff',
            fontSize: 12
          }
        },
        radar: {
          indicator: this.data.indicator,
          center: ['50%', '65%'],
          radius: "60%",
          startAngle: 90,
          splitNumber: 4,
          shape: 'circle',
          name: {
            textStyle: {
              color: 'rgba(255, 255, 255, 0.6)',
              fontSize: 8,
              fontWeight: 'normal'
            }
          },
          axisNameGap: 3,
          splitArea: {
            areaStyle: {
              color: ['#1166C4', '#0C52A4', '#102F7D', '#13216B']
            }
          },
          axisLine: {
            lineStyle: { color: '#163794' }
          },
          splitLine: {
            show: false,
            lineStyle: { color: '#163794' }
          }
        },
        series: {
          name: '雷达图',
          type: 'radar',
          emphasis: {
            lineStyle: { width: 4 }
          },
          data: seriesData
        }
      };

      if (!this.myChart) {
        this.myChart = this.$echarts(this.$el);
      }

      this.myChart.clear();
      this.myChart.resize({
        width: this.$el.offsetWidth,
        height: this.$el.offsetHeight
      });
      this.myChart.setOption(option);
    },

    // ✅ 暴露下载方法（供 EightRadarCharts.vue 调用）
    downloadChart(filename = 'radar.png') {
      if (!this.myChart) return;
      const url = this.myChart.getDataURL({
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
    this.setChart();
  }
}
</script>
