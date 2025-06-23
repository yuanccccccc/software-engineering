<template>
  <Row class="ig-center">
    <!-- 左列 -->
    <Col :span="7">
      <div class="left">
        <span class="title"
          ><span class="title-gradient">鱼群生长情况</span></span
        >
        <span class="angle1"></span>
        <span class="angle2"></span>
        <span class="angle3"></span>
        <span class="angle4"></span>
        <div class="left1" style="height: 44%">
          <div>
            <span class="angle1"></span>
            <span class="angle2"></span>
            <span class="angle3"></span>
            <span class="angle4"></span>
            <div class="fish-boxplot-wrapper">
              <FishBoxPlot />
            </div>
          </div>
        </div>
        <div class="left1" style="height: 50%">
          <div>
            <span class="title"
              ><span class="title-gradient">AI决策</span></span
            >
            <span class="angle1"></span>
            <span class="angle2"></span>
            <span class="angle3"></span>
            <span class="angle4"></span>
            <Advice />
          </div>
        </div>
      </div>
    </Col>

    <!-- 中列 -->
    <Col :span="9" style="padding: 0 1%">
      <div class="center-top">
        <div class="video-container">
          <div>
            <span class="title"
              ><span class="title-gradient">鱼类图像识别</span></span
            >
            <span class="angle1"></span>
            <span class="angle2"></span>
            <span class="angle3"></span>
            <span class="angle4"></span>
          </div>
          <video
            ref="videoPlayer"
            autoplay
            loop
            muted
            playsinline
            class="video-player"
          >
            <source src="@/assets/videos/v_fish.mp4" type="video/mp4" />
            您的浏览器不支持HTML5视频
          </video>
        </div>
      </div>
      <div class="center-bottom">
        <!-- <span class='title'><span class="title-gradient">模块二分析</span></span> -->
        <span class="angle1"></span>
        <span class="angle2"></span>
        <span class="angle3"></span>
        <span class="angle4"></span>
        <view-fish></view-fish>
      </div>
    </Col>

    <!-- 右列 -->
    <Col :span="8">
      <div class="right-2">
        <div class="right1-1">
          <span class="title"
            ><span class="title-gradient">鱼群体重分布</span></span
          >
          <span class="angle1"></span>
          <span class="angle2"></span>
          <span class="angle3"></span>
          <span class="angle4"></span>
          <FishWeight style="height: 100%" />
        </div>
      </div>
      
      <!-- 修改后的右列下侧：球和饼图并排 -->
      <div class="right-3">
        <div class="right3-container">
          <!-- 球区域 -->
          <div class="energy-orb-section">
            <EnergyOrb />
          </div>
          
          <!-- 饼图区域 -->
          <div class="pie-chart-section">
            <div class="pie-chart-wrapper">
              <span class="title"
                ><span class="title-gradient">鱼群数量占比</span></span
              >
              <span class="angle1"></span>
              <span class="angle2"></span>
              <span class="angle3"></span>
              <span class="angle4"></span>
              <FishPieChart style="height: 100%" />
            </div>
          </div>
        </div>
      </div>
    </Col>
  </Row>
</template>

<script>
import ViewFish from "./components/ig_center/viewfish";
import FishPieChart from "./components/ig_center/FishPieChart";
import FishWeight from "./components/ig_center/FishWeight";
import Alarm from "./components/ig_center/Alarm";
import Advice from "./components/ig_center/AI_advice";
import FishBoxPlot from "./components/ig_center/FishBoxPlot";
import EnergyOrb from "./components/ig_center/EnergyOrb";

export default {
  name: "ig-center",
  components: {
    ViewFish,
    FishPieChart,
    FishWeight,
    Alarm,
    Advice,
    FishBoxPlot,
    EnergyOrb,
  },
  data() {
    return {};
  },
  mounted() {
    window.addEventListener("resize", this.resizeFn);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.resizeFn);
  },
  methods: {
    resizeFn() {
      // 窗口大小改变时的处理逻辑
      console.log("Window resized");
    },
  },
};
</script>

<style lang="less" scoped>
.ig-center {
  height: 100%;
  width: 100%;
  padding: 14px 20px 20px;
  background: #03044a;
  overflow: hidden;
  .ivu-col {
    height: 100%;
  }

  .left,
  .right1-1,
  .center-bottom {
    height: 100%;
    border: 1px solid #0d2451;
    position: relative;
    background: #151456;

    #left_5 {
      height: 100%;
      width: 45%;
      float: left;
    }

    #left_6 {
      height: 100%;
      width: 55%;
      float: left;
    }

    .left1 {
      border-bottom: 1px solid #0d2451;
      background: #151456;
    }
  }

  // center
  .center-top {
    height: 61%;
  }

  .video-container {
    width: 100%;
    height: 100%;
    position: relative;
    background: #0d1341;
    border: 3px solid #0d2451;
    display: flex;
    flex-direction: column;
  }
  .video-player {
    flex: 1;
    width: 100%;
    object-fit: contain;
  }

  .center-bottom {
    margin-top: 2%;
    height: 37.5%;
    display: flex;
    flex-direction: column;

    .title {
      z-index: 1;
      position: relative;
      padding: 0 10px;
    }

    view-fish {
      flex: 1;
      margin-top: 10px;
    }
  }

  .right-1 {
    height: 22%;

    .right1-1 {
      height: 100%;
    }
  }

  .right-2 {
    height: 58%;

    .right1-1 {
      height: 97%;
    }
  }

  .right-3 {
    height: 42%;
    
    .right3-container {
      height: 100%;
      display: flex;
      gap: 8px; // 球和饼图之间的间距
    }
    
    .energy-orb-section {
      width: 35%; // 球占35%宽度
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
      // 背景样式
      border: 1px solid #0d2451;
      background: #151456;
      position: relative;
    }
    
    .pie-chart-section {
      flex: 1; // 饼图占剩余宽度
      height: 100%;
      
      .pie-chart-wrapper {
        height: 100%;
        border: 1px solid #0d2451;
        position: relative;
        background: #151456;
      }
    }
  }
}
</style>

<style scoped>
.fish-boxplot-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 10%;
  /* margin: 2rem auto; */
  /* padding: 1.5rem; */
  max-width: 1000px;
  /* background-color: #181753; */
}
</style>
