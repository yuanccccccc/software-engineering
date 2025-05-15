<template>
  <div class="fish-pie-chart-container">
    <div id="fish-pie-chart" ref="chartContainer" class="chart-container"></div>
    <div class="legend-container" v-if="speciesData.length > 0">
      <div v-for="(item, index) in speciesData" :key="index" class="legend-item">
        <div class="color-box" :style="{ backgroundColor: chartColors[index % chartColors.length] }"></div>
        <span class="species-name">{{ item.name }}</span>
        <span class="species-count">({{ item.value }})</span>
      </div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import Papa from 'papaparse';

export default {
  name: 'FishPieChart',
  data() {
    return {
      chartInstance: null,
      speciesData: [],
      chartColors: [
        '#36CBCB', '#4BFFB5', '#2376FE', '#975FE4', 
        '#F7B500', '#FF7A45', '#FF4B4B', '#722ED1'
      ]
    };
  },
  mounted() {
    this.loadCSVData();
    window.addEventListener('resize', this.resizeChart);
  },
  beforeDestroy() {
    if (this.chartInstance) {
      this.chartInstance.dispose();
    }
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    loadCSVData() {
      // 从public目录读取CSV文件
      fetch('/fish_given.csv')
        .then(response => {
          if (!response.ok) {
            throw new Error('Failed to load CSV data');
          }
          return response.text();
        })
        .then(csvText => {
          // 使用Papaparse解析CSV数据
          const parsedData = Papa.parse(csvText, {
            header: true,
            skipEmptyLines: true,
            dynamicTyping: true
          });
          
          // 处理解析后的数据
          this.processData(parsedData.data);
        })
        .catch(error => {
          console.error('Error loading or parsing CSV:', error);
        });
    },
    processData(data) {
      // 统计各种鱼的数量
      const speciesCount = {};
      
      data.forEach(row => {
        const species = row.Species;
        if (species) {
          speciesCount[species] = (speciesCount[species] || 0) + 1;
        }
      });
      
      // 转换为图表所需的数据格式
      this.speciesData = Object.keys(speciesCount).map(species => ({
        name: species,
        value: speciesCount[species]
      }));
      
      // 初始化图表
      this.$nextTick(() => {
        this.initChart();
      });
    },
    initChart() {
      const chartDom = this.$refs.chartContainer;
      this.chartInstance = echarts.init(chartDom);
      
      const option = {
        backgroundColor: 'transparent',
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        series: [
          {
            name: '鱼类分布',
            type: 'pie',
            radius: ['40%', '70%'],
            center: ['50%', '50%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 4,
              borderColor: '#151456',
              borderWidth: 2
            },
            label: {
              show: false
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '14',
                fontWeight: 'bold',
                color: '#ffffff'
              }
            },
            labelLine: {
              show: false
            },
            data: this.speciesData,
            color: this.chartColors
          }
        ]
      };
      
      this.chartInstance.setOption(option);
    },
    resizeChart() {
      if (this.chartInstance) {
        this.chartInstance.resize();
      }
    }
  }
};
</script>

<style scoped>
.fish-pie-chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 10px;
}

.chart-container {
  flex: 3;
  width: 100%;
}

.legend-container {
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  padding: 0 10px;
}

.legend-item {
  display: flex;
  align-items: center;
  margin: 5px 10px;
}

.color-box {
  width: 12px;
  height: 12px;
  margin-right: 6px;
  border-radius: 2px;
}

.species-name {
  color: #ffffff;
  font-size: 12px;
  margin-right: 4px;
}

.species-count {
  color: #36CBCB;
  font-size: 12px;
}
</style>