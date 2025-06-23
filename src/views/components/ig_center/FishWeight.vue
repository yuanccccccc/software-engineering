<template>
  <div class="fish-chart-container">
    <div class="chart-wrapper">
      <div class="fish-chart" ref="chartContainer"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from 'echarts';
import Papa from 'papaparse';

export default {
  name: 'FishDataVisualization',
  data() {
    return {
      chart: null,
      fishData: [],
      speciesList: [],
      isLoading: true,
      colorMap: {
        'Bream': '#FF6384',
        'Roach': '#36A2EB',
        'Whitefish': '#FFCE56',
        'Parkki': '#4BC0C0',
        'Perch': '#9966FF',
        'Pike': '#FF9F40',
        'Smelt': '#32CD32'
      }
    };
  },
  mounted() {
    this.loadFishData();
    window.addEventListener('resize', this.resizeChart);
    // 在元素挂载后设置尺寸
    this.$nextTick(() => {
      this.resizeChart();
    });
  },
  beforeDestroy() {
    if (this.chart) {
      this.chart.dispose();
    }
    window.removeEventListener('resize', this.resizeChart);
  },
  methods: {
    loadFishData() {
      this.isLoading = true;
      
      Papa.parse('/fish_given.csv', {
        download: true,
        header: true,
        dynamicTyping: true,
        skipEmptyLines: true,
        complete: (results) => {
          this.fishData = results.data;
          
          // Extract unique species
          this.speciesList = [...new Set(this.fishData.map(item => item.Species))];
          
          this.processDataAndRenderWeightChart();
          this.isLoading = false;
        },
        error: (error) => {
          console.error('Error loading fish data:', error);
          this.isLoading = false;
        }
      });
    },
    
    processDataAndRenderWeightChart() {
      if (!this.fishData.length) return;
      
      // Group data by species and prepare for visualization
      const seriesData = this.speciesList.map(species => {
        // Filter data for the current species
        const fishOfSpecies = this.fishData.filter(fish => fish.Species === species);
        
        // Sort by weight for smooth curve
        fishOfSpecies.sort((a, b) => a['Weight(g)'] - b['Weight(g)']);
        
        // Generate bins for weight distribution
        const bins = this.generateBins(fishOfSpecies, 'Weight(g)');
        
        return {
          name: species,
          type: 'line',
          smooth: true,
          symbolSize: 0,
          lineStyle: {
            width: 2
          },
          data: bins.map(bin => [bin.value, bin.count]),
          color: this.colorMap[species] || '#' + Math.floor(Math.random()*16777215).toString(16)
        };
      });
      
      this.renderChart(seriesData);
    },
    
    generateBins(data, valueProp) {
      // Get value range
      const values = data.map(item => item[valueProp]);
      const minValue = Math.min(...values);
      const maxValue = Math.max(...values);
      
      // Create bins
      const binSize = (maxValue - minValue) / 15; // Adjust bin size for smoothness
      const bins = [];
      
      for (let i = minValue; i <= maxValue; i += binSize) {
        const binEnd = i + binSize;
        const itemsInBin = data.filter(item => 
          item[valueProp] >= i && item[valueProp] < binEnd
        );
        
        bins.push({
          value: i,
          count: itemsInBin.length
        });
      }
      
      return bins;
    },
    
    renderChart(seriesData, xAxisName) {
      // Initialize chart if container exists
      if (!this.$refs.chartContainer) return;
      
      // Create or re-use chart instance
      if (!this.chart) {
        this.chart = echarts.init(this.$refs.chartContainer);
      }
      
      const option = {
        backgroundColor: 'transparent', // 透明背景
        tooltip: {
          trigger: 'axis',
          confine: true, // 确保提示框在图表区域内
          formatter: function(params) {
            const param = params[0];
            return `${param.seriesName}<br/>体重: ${param.value[0].toFixed(1)}g<br/>数量: ${param.value[1]}`;
          },
          textStyle: {
            fontSize: 10
          }
        },
        legend: {
          data: this.speciesList,
          textStyle: {
            color: '#ffffff',
            fontSize: 10
          },
          top: 15,
          type: 'scroll',
          orient: 'horizontal',
          left: 'center',
          itemGap: 8,
          // 设置为两行显示
          pageButtonPosition: 'end',
          itemWidth: 15,
          itemHeight: 10,
          pageButtonSize: 10,
          pageButtonGap: 3,
          pageIconSize: 8,
          pageIconColor: '#ffffff',
          pageIconInactiveColor: '#666666',
          pageTextStyle: {
            color: '#ffffff',
            fontSize: 8
          }
        },
        grid: {
          left: '5%',
          right: '5%',
          bottom: '5%',
          top: 45,
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: xAxisName,
          nameTextStyle: {
            color: '#ffffff',
            fontSize: 10,
            padding: [0, 0, 0, 5]
          },
          axisLabel: {
            color: '#ffffff',
            fontSize: 9,
            margin: 6
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          }
        },
        yAxis: {
          type: 'value',
          nameTextStyle: {
            color: '#ffffff',
            fontSize: 10,
            padding: [0, 0, 5, 0]
          },
          axisLabel: {
            color: '#ffffff',
            fontSize: 9,
            margin: 6
          },
          splitLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          },
          axisLine: {
            lineStyle: {
              color: 'rgba(255, 255, 255, 0.3)'
            }
          }
        },
        series: seriesData
      };
      
      this.chart.setOption(option, true);
    },
    
    resizeChart() {
      if (this.chart) {
        this.chart.resize();
      }
    }
  }
};
</script>

<style scoped>
.fish-chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chart-wrapper {
  margin-top: 10px;
  flex: 1;
  width: 100%;
  overflow: hidden;
}

.fish-chart {
  width: 100%;
  height: 100%;
}
</style>