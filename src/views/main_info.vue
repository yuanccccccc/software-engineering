<template>
    <div class="main_info">
        <!-- 上半部分65% -->
        <Row class='content'>

            <!-- 左列：视频展示 -->
            <Col span="11">
                <div class="video-container">
                    <div>
                        <span class='title'><span class="title-gradient">视频展示</span></span>
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
                        <source src="@/assets/videos/v_mainpage.mp4" type="video/mp4">
                        您的浏览器不支持HTML5视频
                    </video>
                </div>
            </Col>

            <!-- 中列 -->
            <Col span="6" style="padding:0 1%;height:90%;">
                <div class="middle-container">
                    <div>
                        <span class='title'><span class="title-gradient">水文数据</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                    </div>
                    <div class="hydrological-chart">
                        <water-data-chart 
                            :data="hydrologicalData"
                        ></water-data-chart>
                    </div>
                </div>
            </Col>


            <!-- 右列 -->
            <Col span="7" style="height:90%;">
                <div class="map-container" style="height:100%;background:#0D1341;border:3px solid #0D2451;">
                    <china-map ref="chinaMap" style="width:100%;height:100%"></china-map>
                </div>
            </Col>
        </Row>

        <!-- 下半部分35% -->
        <Row class="bottom-list">
            <Col span="5">
                <div class="list right-bottom">
                    <div class="bottom">
                        <span class='title'><span class="title-gradient">天气实况</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <weather-info></weather-info>
                    </div>
                </div>

            </Col>

            <Col span="10">
                <div class="list right-bottom">
                    <div class="bottom">
                        <span class='title'><span class="title-gradient">天气预报</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <forecast></forecast>
                    </div>
                </div>
            </Col>

            <Col span="9">
                <div class="list right-bottom">
                    <div class="bottom">
                        <span class='title'><span class="title-gradient">设备与预警</span></span>
                        <span class="angle1"></span>
                        <span class="angle2"></span>
                        <span class="angle3"></span>
                        <span class="angle4"></span>
                        <device-info></device-info>
                    </div>
                </div>
            </Col>
        </Row>
    </div>
</template>

<script>
// import axios from "axios";
const chinaMap  = () => import('./components/main_info/chinaMap');
// const waterDataChart = () => import('./components/main_info/waterDataChart');
// const weatherInfo = () => import('./components/main_info/weatherInfo');
// const forecast = () => import('./components/main_info/forecast');
// const deviceInfo = () => import('./components/main_info/device');

export default {
    name: "main_info",
    components: {
        chinaMap: () => import('./components/main_info/chinaMap'),
        waterDataChart: () => import('./components/main_info/waterDataChart'),
        weatherInfo: () => import('./components/main_info/weatherInfo'),
        forecast: () => import('./components/main_info/forecast'),
        deviceInfo: () => import('./components/main_info/device'),
    },
    data() {
        return {
            hydrologicalData: [
                {
                    subtitle: '水温',
                    unit: '℃',
                    min: 0,
                    max: 40,
                    data: {
                        name: '水温',
                        value: 23.5,
                        color: '#0DF5F8'
                    }
                },
                {
                    subtitle: 'pH值',
                    unit: '',
                    min: 0,
                    max: 14,
                    data: {
                        name: 'pH值',
                        value: 7.2,
                        color: '#0B8DFF'
                    }
                },
                {
                    subtitle: '溶解氧',
                    unit: 'mg/L',
                    min: 0,
                    max: 20,
                    data: {
                        name: '溶解氧',
                        value: 8.6,
                        color: '#00FFCC'
                    }
                },
                {
                    subtitle: '浊度',
                    unit: 'NTU',
                    min: 0,
                    max: 50,
                    data: {
                        name: '浊度',
                        value: 5.3,
                        color: '#FFB800'
                    }
                },
                {
                    subtitle: '叶绿素α',
                    unit: 'μg/L',
                    min: 0,
                    max: 10,
                    data: {
                        name: '叶绿素α',
                        value: 3.7,
                        color: '#41B883'
                    }
                },
                {
                    subtitle: '藻密度',
                    unit: 'cells/L',
                    min: 0,
                    max: 5000,
                    data: {
                        name: '藻密度',
                        value: 1250,
                        color: '#FF6464'
                    }
                }
            ]
        }
    },
    mounted() {
        this.$nextTick(() => {
            this.$refs.chinaMap.initMap();
        });
        this.resizeFn = this.$debounce(() => {
            this.$refs.chinaMap.setMap();
        }, 500);
        window.addEventListener('resize', this.resizeFn);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn);
    }
}

</script>

<style lang="less" scoped>
.main_info {
    height: 100%;
    width: 100%;
    padding: 14px 20px 20px;
    background: #03044A;
    overflow: hidden;

    .content {
        height: 65%;

        /* 视频样式 */
        .video-container {
            width: 100%;
            height: 100%;
            position: relative;
            background: #0D1341;
            border: 3px solid #0D2451;
            display: flex;
            flex-direction: column;
        }

        /* 中列样式 */
        .middle-container {
            width: 100%;
            height: 100%;
            position: relative;
            background: #0D1341;
            border: 3px solid #0D2451;
            display: flex;
            flex-direction: column;
            
            .hydrological-chart {
                flex: 1;
                width: 100%;
                height: calc(100% - 50px);
                padding: 5px;
            }
        }
    }

    .bottom-list {
        height: 35%;

        .ivu-col {
            height: 100%;

            .list {
                height: 100%;
                width: 33.3333%;
                padding-right: 1.5%;
                float: left;
                .bottom {
                    width: 100%;
                    height: 100%;
                    border: 1px solid #0D2451;
                    position: relative;
                }
            }

            .right-bottom {
                width: 100%;
                padding-right: 0;
            }
        }
    }
    

}
</style>