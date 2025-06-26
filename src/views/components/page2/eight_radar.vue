<template>
  <div class="eight-radar-wrapper">
    <!-- ✅ 下载按钮：统一导出8张图 -->
    <button @click="downloadAllRadarCharts" class="download-btn">
      下载图表
    </button>

    <Row class="bottom-radars" :gutter="10" type="flex">
      <Col
        v-for="(item, index) in radarData.slice(0, 4)"
        :key="'r1-' + index"
        span="6"
      >
        <div class="radar-container">
          <Radar
            :id="'radar_top_' + index"
            :data="item"
            :ref="'radar' + index"
          />
        </div>
      </Col>
    </Row>
    <Row class="bottom-radars" :gutter="10" type="flex">
      <Col
        v-for="(item, index) in radarData.slice(4, 8)"
        :key="'r2-' + index"
        span="6"
      >
        <div class="radar-container">
          <Radar
            :id="'radar_bottom_' + index"
            :data="item"
            :ref="'radar' + (index + 4)"
          />
        </div>
      </Col>
    </Row>
  </div>
</template>

<script>
import axios from "axios";
import Radar from "../radar.vue";

export default {
  name: "EightRadarCharts",
  components: {
    Radar,
  },
  data() {
    return {
      radarData: [],
    };
  },
  mounted() {
    axios
      .get("http://localhost:5000/api/eight_radar")
      .then((res) => {
        this.radarData = res.data;
      })
      .catch((err) => {
        console.error("雷达图数据加载失败：", err);
      });
  },
  methods: {
    // ✅ 下载所有雷达图
    downloadAllRadarCharts() {
      for (let i = 0; i < 8; i++) {
        const refArray = this.$refs["radar" + i];
        const refComp = Array.isArray(refArray) ? refArray[0] : refArray;
        if (refComp && typeof refComp.downloadChart === "function") {
          refComp.downloadChart(`radar_chart_${i + 1}.png`);
        } else {
          console.warn(`⚠️ radar${i} not found or missing downloadChart method`);
        }
      }
    },
  },
};
</script>

<style scoped>
.eight-radar-wrapper {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  position: relative;
}

.bottom-radars {
  flex: 1;
  display: flex;
  margin-bottom: 20px;
}

.radar-container {
  height: 100%;
  width: 100%;
}

/* ✅ 下载按钮样式 */
.download-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(92, 169, 230, 0.6);
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  z-index: 100;
  font-size: 12px;
  transition: background 0.3s ease;
}

.download-btn:hover {
  background: rgba(92, 169, 230, 0.9);
}
</style>
