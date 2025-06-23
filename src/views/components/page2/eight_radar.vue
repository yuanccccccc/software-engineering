<template>
  <div class="eight-radar-wrapper">
    <Row class="bottom-radars" :gutter="[4, 10]" type="flex">
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
    <Row class="bottom-radars" :gutter="[4, 10]" type="flex">
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

<style scoped>
.eight-radar-wrapper {
  height: 100%; /* 让整个雷达图区域填满父容器 */
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.bottom-radars {
  flex: 1; /* 上下两行平均占空间 */
  display: flex;
}

.radar-container {
  height: 100%;
  width: 100%;
}
</style>

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
};
</script>

<style scoped>
.bottom-radars {
  margin-bottom: 20px;
}
</style>
