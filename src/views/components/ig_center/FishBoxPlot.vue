<template>
  <div class="fish-boxplot">
    <div class="chart-controls">
      <label class="chart-type-selector">
        <span class="label-text">显示数据:</span>
        <select id="view-select" v-model="selectedView">
          <option>Species vs Weight</option>
          <option>Dimensions Overview</option>
        </select>
      </label>
    </div>
    <div style="position: relative;">
      <canvas ref="chartCanvas"></canvas>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { Chart, CategoryScale, LinearScale, Tooltip, Title, Legend } from 'chart.js';
import { BoxPlotController, BoxAndWiskers } from '@sgratzl/chartjs-chart-boxplot';
import Papa from 'papaparse';

Chart.register(BoxPlotController, BoxAndWiskers, CategoryScale, LinearScale, Tooltip, Title, Legend);

const chartCanvas = ref(null);
const chartInstance = ref(null);
const selectedView = ref('Species vs Weight');

let speciesList = [];
let weightDataBySpecies = [];
let lengthData = [];
let widthData = [];
let heightData = [];

const generateChartData = (view) => {
  if (view === 'Species vs Weight') {
    return {
      labels: speciesList,
      datasets: [
        {
          label: 'Weight (g)',
          backgroundColor: 'rgba(75,192,192,0.5)',
          borderColor: 'rgb(75,192,192)',
          borderWidth: 1,
          outlierColor: '#ff9900',
          padding: 10,
          itemRadius: 0,
          data: weightDataBySpecies
        }
      ]
    };
  } else if (view === 'Dimensions Overview') {
    return {
      labels: ['Length', 'Width', 'Height'],
      datasets: [
        {
          label: 'Dimensions (cm)',
          backgroundColor: 'rgba(153,102,255,0.5)',
          borderColor: 'rgb(153,102,255)',
          borderWidth: 1,
          outlierColor: '#ff9900',
          padding: 10,
          itemRadius: 0,
          data: [lengthData, widthData, heightData]
        }
      ]
    };
  }
  return { labels: [], datasets: [] };
};

const initChart = () => {
  const ctx = chartCanvas.value.getContext('2d');
  const dataConfig = generateChartData(selectedView.value);
  chartInstance.value = new Chart(ctx, {
    type: 'boxplot',
    data: dataConfig,
    options: {
      responsive: true,
      maintainAspectRatio: true,
      aspectRatio: 1.5,
      plugins: {
        title: {
          display: true,
          text: selectedView.value === 'Species vs Weight'
            ? 'Species vs Weight (g)'
            : 'Dimensions Overview (cm)',
          color: '#ffffff'
        },
        legend: {
          display: false,
          labels: { color: '#ffffff' }
        },
        tooltip: {
          mode: 'nearest',
          intersect: false,
          titleColor: '#ffffff',
          bodyColor: '#ffffff'
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          title: {
            display: true,
            text: selectedView.value === 'Species vs Weight'
              ? 'Weight (g)'
              : 'Measurement (cm)',
            color: '#ffffff'
          },
          ticks: {
            color: '#ffffff'
          }
        },
        x: {
          title: { display: false },
          ticks: {
            color: '#ffffff'
          }
        }
      }
    }
  });
};

const updateChart = () => {
  if (!chartInstance.value) return;
  const newData = generateChartData(selectedView.value);
  chartInstance.value.data.labels = newData.labels;
  chartInstance.value.data.datasets = newData.datasets;
  chartInstance.value.options.plugins.title.text =
    selectedView.value === 'Species vs Weight'
      ? 'Species vs Weight (g)'
      : 'Dimensions Overview (cm)';
  chartInstance.value.options.scales.y.title.text =
    selectedView.value === 'Species vs Weight'
      ? 'Weight (g)'
      : 'Measurement (cm)';
  chartInstance.value.update();
};

onMounted(() => {
  Papa.parse('/fish_given.csv', {
    download: true,
    header: true,
    dynamicTyping: true,
    complete: (results) => {
      const data = results.data;
      const speciesMap = {};
      data.forEach(item => {
        const species = item.Species;
        const weight = item['Weight(g)'];
        const length = item['Length1(cm)'];
        const width = item['Width(cm)'];
        const height = item['Height(cm)'];
        if (species && !isNaN(weight)) {
          if (!speciesMap[species]) speciesMap[species] = [];
          speciesMap[species].push(weight);
        }
        if (!isNaN(length)) lengthData.push(length);
        if (!isNaN(width)) widthData.push(width);
        if (!isNaN(height)) heightData.push(height);
      });
      speciesList = Object.keys(speciesMap);
      weightDataBySpecies = speciesList.map(sp => speciesMap[sp]);
      initChart();
    }
  });
});

watch(selectedView, () => {
  updateChart();
});
</script>

<style scoped>
.fish-boxplot {
  max-width: 800px;
  margin: 0 auto;
}

.chart-controls {
  padding: 20px 10px 0 5px;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 32px;
}

.chart-type-selector {
  display: flex;
  align-items: center;
  color: #ffffff;
  font-size: 14px;
  margin-bottom: 10%;
}

.label-text {
  margin-right: 8px;
  color: #ffffff;
}

select {
  background-color: #151456;
  color: #ffffff;
  border: 1px solid #0D2451;
  border-radius: 3px;
  /* padding: 2px 8px; */
  cursor: pointer;
  outline: none;
  font-size: 13px;
  height: 24px;
}

select:hover {
  background-color: #1a1a66;
}

canvas {
  background-color: transparent !important;
  max-width: 100%;
}
</style>
