<template>
    <Row class="ig-center">

        <!-- 左列 -->
        <Col :span="7">
            <div class="left">
                <span class='title'><span class="title-gradient">鱼群生长情况</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <div class="left1" style="height:47%;">
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
                <div class="left1" style="height:24%;">
                    <div>
                        <span class='title'><span class="title-gradient">AI决策</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <Advice />
                    </div>
                </div>
                <div class="right-1">
                    <div class="right1-1">
                        <span class='title'><span class="title-gradient">预警</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <Alarm />
                    </div>
                </div>
            </div>
        </Col>

        <!-- 中列 -->
        <Col :span="9" style="padding:0 1%;">
            <div class="center-top">
                <div class="video-container">
                    <div>
                        <span class='title'><span class="title-gradient">鱼类图像识别</span></span>
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
                        <source src="@/assets/videos/v_fish.mp4" type="video/mp4">
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
            <!-- <div class="right-1">
                <div class="right1-1">
                    <span class='title'><span class="title-gradient">预警</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <Alarm />
                </div>
            </div> -->
            <div class="right-2">
                <div class="right1-1">
                    <span class='title'><span class="title-gradient">鱼群体重分布</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <FishWeight style="height: 100%;" />
                </div>
            </div>
            <div class="right-3">
                <div class="right1-1">
                    <span class='title'><span class="title-gradient">鱼群数量占比</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <FishPieChart style="height: 100%;" />
                </div>
            </div>
        </Col>
    </Row>
</template>

<script>
import ViewFish from './components/ig_center/viewfish';
import FishPieChart from './components/ig_center/FishPieChart';
import FishWeight from './components/ig_center/FishWeight';
import Alarm from './components/ig_center/Alarm';
import Advice from './components/ig_center/AI_advice';
import FishBoxPlot from './components/ig_center/FishBoxPlot';

export default {
    name: 'ig-center',
    components:{
        ViewFish,
        FishPieChart,
        FishWeight,
        Alarm,
        Advice,
        FishBoxPlot,
    },
    data() {
        return {}
    },
    mounted() {
        window.addEventListener('resize', this.resizeFn);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn);
    },
    methods: {
        resizeFn() {
            // 窗口大小改变时的处理逻辑
            console.log('Window resized');
        }
    }
}
</script>

<style lang="less" scoped>
.ig-center {
    height: 100%;
    width: 100%;
    padding: 14px 20px 20px;
    background: #03044A;
    overflow: hidden;
    .ivu-col {
        height: 100%;
    }

    .left, .right1-1, .center-bottom {
        height: 100%;
        border: 1px solid #0D2451;
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
            border-bottom: 1px solid #0D2451;
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
        background: #0D1341;
        border: 3px solid #0D2451;
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