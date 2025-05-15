<template>
  <div style="position: relative; user-select: none;">
    <div class="filter-buttons" style="margin-bottom:12px; text-align: center;">
      <button
        v-for="species in speciesSet"
        :key="species"
        @mouseenter="highlightSpecies = species"
        @mouseleave="highlightSpecies = ''"
        :style="{
          backgroundColor: highlightSpecies === species ? speciesColorMap[species] : '#ddd',
          color: highlightSpecies === species ? '#fff' : '#333',
          border: 'none',
          padding: '6px 14px',
          margin: '0 6px',
          borderRadius: '4px',
          cursor: 'pointer',
          transition: 'background-color 0.3s,color 0.3s'
        }"
      >
        {{ species }}
      </button>
    </div>

    <div ref="chart" class="chart-container"></div>
  </div>
</template>

<script>
import * as echarts from "echarts";
import "echarts-gl";
import axios from "axios";

export default {
  name: "Fish3DScatterGlassHighlight",
  data() {
    return {
      chart: null,
      rawData: [],
      speciesSet: [],
      highlightSpecies: "",
      speciesColorMap: {},
    };
  },
  mounted() {
    this.chart = echarts.init(this.$refs.chart);
    this.fetchData();
    this.resizeHandler = () => this.chart && this.chart.resize();
    window.addEventListener("resize", this.resizeHandler);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.resizeHandler);
    if (this.chart) this.chart.dispose();
  },
  watch: {
    highlightSpecies() {
      this.renderChart();
    },
  },
  methods: {
    async fetchData() {
      try {
        const res = await axios.get("http://localhost:5000/api/fish_data");
        this.rawData = res.data;
        this.speciesSet = [...new Set(this.rawData.map((d) => d.Species))];
        const baseColors = [
          "#5470C6",
          "#91CC75",
          "#FAC858",
          "#EE6666",
          "#73C0DE",
          "#3BA272",
          "#FC8452",
        ];
        this.speciesSet.forEach((sp, idx) => {
          this.speciesColorMap[sp] = baseColors[idx % baseColors.length];
        });
        this.renderChart();
      } catch (error) {
        console.error("请求鱼类数据失败", error);
      }
    },

    renderChart() {
      if (!this.rawData.length) return;

      const dataPoints = this.rawData.map((item) => {
        const avgLength =
          (item["Length1(cm)"] + item["Length2(cm)"] + item["Length3(cm)"]) / 3;
        return [
          avgLength,
          item["Width(cm)"],
          item["Height(cm)"],
          item["Weight(g)"],
          item["Species"],
        ];
      });

      const series = this.speciesSet.map((species) => {
        const isHighlight =
          !this.highlightSpecies || this.highlightSpecies === species;
        return {
          name: species,
          type: "scatter3D",
          data: dataPoints
            .filter((d) => d[4] === species)
            .map((d) => [d[0], d[1], d[2], d[3]]),
          symbolSize: (val) => {
            const size = val[3] / 30;
            return Math.min(Math.max(size, 6), 40);
          },
          itemStyle: {
            color: this.speciesColorMap[species],
            opacity: isHighlight ? 1 : 0.15,
            borderWidth: isHighlight ? 3 : 0,
            borderColor: isHighlight ? "#000" : null,
          },
          emphasis: {
            label: { show: false },
          },
        };
      });

      const photonParticles = Array.from({ length: 50 }, () => {
        return {
          type: "circle",
          shape: {
            r: Math.random() * 2 + 1,
          },
          style: {
            fill: "rgba(255,255,255,0.6)",
            shadowBlur: 6,
            shadowColor: "rgba(255,255,255,0.8)",
          },
          left: `${Math.random() * 100}%`,
          top: `${Math.random() * 100}%`,
          z: 2,
          silent: true,
        };
      });

      const graphicOverlay = [
        {
          type: "rect",
          left: "14%",
          top: "66%",
          shape: {
            width: "72%",
            height: "29%",
          },
          style: {
            fill: "rgba(200, 230, 255, 0.35)",
            stroke: "rgba(255, 255, 255, 0.4)",
            lineWidth: 1,
            cursor: "default",
          },
          silent: true,
          z: 1,
        },
        ...photonParticles, // 已删除中间白圈，仅保留光子
      ];

      const option = {
        backgroundColor: {
          type: "linear",
          x: 0,
          y: 0,
          x2: 0,
          y2: 1,
          colorStops: [
            { offset: 0, color: "#d7e1f9" },
            { offset: 1, color: "#f9fbfe" },
          ],
        },
        title: {
          text: "鱼类三维尺寸分布（均长、宽、高）",
          left: "center",
          textStyle: { color: "#333", fontSize: 22 },
        },
        tooltip: {
          formatter: (params) => {
            const [avgLength, width, height, weight] = params.value;
            return `
              <b>${params.seriesName}</b><br/>
              平均长度: ${avgLength.toFixed(2)} cm<br/>
              宽度: ${width.toFixed(2)} cm<br/>
              高度: ${height.toFixed(2)} cm<br/>
              体重: ${weight.toFixed(2)} g
            `;
          },
        },
        legend: {
          show: true,
          bottom: 10,
          data: this.speciesSet,
          textStyle: { color: "#555" },
          selectedMode: "multiple",
          selected: this.speciesSet.reduce((obj, sp) => {
            obj[sp] = true;
            return obj;
          }, {}),
        },
        grid3D: {
          boxWidth: 100,
          boxDepth: 100,
          boxHeight: 60,
          light: {
            main: { intensity: 0 },
            ambient: { intensity: 0 },
          },
          axisPointer: { show: false },
          viewControl: {
            autoRotate: true,
            autoRotateSpeed: 5,
            rotateSensitivity: 1.5,
            zoomSensitivity: 1.2,
            panSensitivity: 1,
          },
          splitArea: {
            show: true,
            areaStyle: {
              color: [
                "rgba(255,255,255,0.15)",
                "rgba(200,200,255,0.08)",
              ],
            },
          },
        },
        xAxis3D: {
          name: "平均长度 (cm)",
          axisLine: { lineStyle: { color: "rgba(150,150,150,0.3)" } },
          splitLine: { lineStyle: { color: "rgba(150,150,150,0.1)" } },
          axisLabel: { color: "rgba(50,50,50,0.7)" },
        },
        yAxis3D: {
          name: "宽度 (cm)",
          splitLine: { lineStyle: { color: "rgba(150,150,150,0.1)" } },
          axisLine: { lineStyle: { color: "#666" } },
          axisLabel: { color: "#333" },
        },
        zAxis3D: {
          name: "高度 (cm)",
          splitLine: { lineStyle: { color: "rgba(150,150,150,0.1)" } },
          axisLine: { lineStyle: { color: "#666" } },
          axisLabel: { color: "#333" },
        },
        series,
        graphic: graphicOverlay,
      };

      this.chart.setOption(option);
    },
  },
};
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 70vh;
  min-height: 450px;
}
.filter-buttons {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 8px;
}
.filter-buttons button {
  padding: 6px 14px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  background-color: #ddd;
  color: #333;
  transition: all 0.3s;
  user-select: none;
}
.filter-buttons button:hover {
  opacity: 0.8;
}
</style>
