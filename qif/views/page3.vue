<template>
    <Row class="page3">
        <Col :span="7">
            <div class="left">
                <span class='title'><span class="title-text">各省份水质分析</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <div class="left1" style="height:50%;">
                    <div style="height:65%;">
                        <MyWaterChart id="left_1" />
                    </div>
                    <div style="height: 35%;display: flex">
                        <div style="height: 100%; width: 33.33%;">
                            <pie ref="chart3" id="pie_1" :data="pieData1"></pie>
                        </div>
                        <div style="height: 100%; width: 33.33%;">
                            <pie ref="chart3" id="pie_3" :data="pieData2"></pie>
                        </div>
                        <div style="height: 100%; width: 33.33%;">
                            <pie ref="chart3" id="pie_2" :data="pieData3"></pie>
                        </div>
                    </div>
                </div>
                <div class="left1" style="height:50%;">
                    <phtChart id="left_1" />
                </div>
            </div>
        </Col>
        <Col :span="10" style="padding:0 1%;">
            <div class="center-top">
                <china-map ref="chinaMap"></china-map>
            </div>
            <div class="center-bottom">
                <span class='title'><span class="title-text">流域内水质等级分布</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <EightRadarCharts />
            </div>
        </Col>
        <Col :span="7">
            <div class="right-1">
                <div class="right1-1">
                    <span class='title'><span class="title-text">历史数据分析</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <WaterQualityChart />
                </div>
            </div>
            <div class="right-2">
                <div class="right1-1">
                    <span class='title'><span class="title-text">站点情况</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <tableaa />
                </div>
            </div>
        </Col>
    </Row>
</template>

<script>
import axios from 'axios'
const chinaMap  = () => import('./components/page3/chinaMap');
const pie = ()=> import('./components/pie');
const radar = ()=> import('./components/radar');
const MyWaterChart = () => import('./components/page3/temp');
const phtChart = () => import('./components/page3/pht');
const EightRadarCharts = () => import('./components/page3/eight_radar')
const WaterQualityChart = () => import('./components/page3/line');
const tableaa = () => import('./components/page3/table');
export default {
    name: 'page3',
    components: {
        chinaMap,
        MyWaterChart,
        pie,
        phtChart,
        EightRadarCharts,
        WaterQualityChart,
        tableaa
        
    },
    data() {
        return {
            pieData1: null,
            pieData2: null,
            pieData3: null,
            resizeFn: null
        }
    },
    async mounted() {
        const response = await axios.get("http://localhost:5000/api/pie_data")
        const pieList = response.data
        this.pieData1 = pieList[0] || { data: [] }
        this.pieData2 = pieList[1] || { data: [] }
        this.pieData3 = pieList[2] || { data: [] }
        this.$nextTick(() => {
            this.$refs.chart3[0]?.setChart()
            this.$refs.chart3[1]?.setChart()
            this.$refs.chart3[2]?.setChart()
        })


        this.resizeFn = this.$debounce(()=> {
            // 通过捕获系统的onresize事件触发我们需要执行的事件
           //this.$refs.channelBar1.setChart();
           this.$refs.distributionSolider1.setChart();
           this.$refs.channelBar2.setChart();
           this.$refs.distributionSolider2.setChart();
            //this.$refs.pies.setPies();
           this.$refs.redPocket.setPocket();
           this.$refs.webcastsRisk.setWebcasts();
           this.$refs.deviceSafeRisk.setDeviceSafe();
           this.$refs.ring1.drawRing();
           this.$refs.ring2.drawRing();
           this.$refs.ring3.drawRing();
            for (let i = 2; i < 9; i++) {
               this.$refs['chart' + i].setChart()

            }
           this.$refs.chinaMap.setMap();
           this.$refs.hotWords.setChart();

        }, 500)
        window.addEventListener('resize', this.resizeFn)
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn)
    }
}
</script>

<style lang="less" scoped>
.page3 {
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

        .circular {
            height: 100%;

            .canvas {
                height: 100%;
                width: 30%;
                float: left;

                .subtitle {
                    font-size: 12px;
                    font-weight: bold;
                    color: #fff;
                    height: 25px;
                    padding: 10px 0 ;
                    text-align: center;
                }

                .canvasList {
                    height: calc(~'100% - 25px');
                    text-align: center
                }
            }
        }

        .left1 {
            border-bottom: 1px solid #0D2451;
            background: #151456;
        }

        .title {
            position: absolute;
            display: inline-block;
            color: #6EDDF1;
            border: 2px solid #6EDDF1;
            height: 18px;
            padding: 0 2px;
            left: 50%;
            transform: translate(-50%, -50%);

            .title-text {
                position: relative;
                font-size: 16px;
                background: #09102E;
                display: inline-block;
                padding: 0 4px;
                transform: translateY(-5px);
            }
        }
    }

    .center-top {
        height: 60%;
    }

    .center-bottom {
        height: 40%;

        .bottom-radars {
            height: 55%;
        }

        .bottom-bars {
            height: 45%;
        }
    }

    .right-1 {
        height: 70%;

        .right1-1 {
            height: 92%;
        }
    }

    .right-2 {
        height: 30%;

    }
}
</style>
