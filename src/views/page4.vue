<template>
  <div class="page1-container">
    <!-- 动态波浪背景canvas -->
    <canvas ref="backgroundCanvas" class="background-canvas"></canvas>

    <!-- 中间大图 -->
    <div class="center-chart">
      <FishBoxPlot />
    </div>
    <!-- 左侧悬浮图 -->
    <div class="floating-chart left">
      <FishViolinPlot />
      <!-- 在左侧悬浮图下方添加导出浮窗 -->
      
      <FishLengthPredictor /> 
    </div>
    <!-- 右侧悬浮图 -->
    <div class="floating-chart right">
      <FishChart />
      <ExportFloatWindow />  <!-- 这里放预测模块 -->
    </div>
  </div>
</template>

<script>
import FishBoxPlot from '@/components/FishBoxPlot.vue';
import FishViolinPlot from '@/components/FishViolinPlot.vue';
import FishChart from '@/components/FishChart.vue';
import ExportFloatWindow from '@/components/ExportFloatWindow.vue';
import FishLengthPredictor from '@/components/page4/FishLengthPredictor.vue';

export default {
  name: 'Page1Charts',
  components: {
    FishBoxPlot,
    FishViolinPlot,
    ExportFloatWindow,  // 注册浮窗组件
    FishLengthPredictor,
    FishChart
  },
  mounted() {
    this.initCanvasWaves();
  },
  methods: {
    initCanvasWaves() {
      const canvas = this.$refs.backgroundCanvas;
      const ctx = canvas.getContext('2d');
      const dpr = window.devicePixelRatio || 1;

      function resize() {
        canvas.width = canvas.clientWidth * dpr;
        canvas.height = canvas.clientHeight * dpr;
        ctx.scale(dpr, dpr);
      }
      resize();
      window.addEventListener('resize', resize);

      let time = 0;

      function drawWave() {
        const width = canvas.clientWidth;
        const height = canvas.clientHeight;
        ctx.clearRect(0, 0, width, height);

        // 第一条波浪
        ctx.fillStyle = 'rgba(0, 120, 200, 0.15)';
        ctx.beginPath();
        ctx.moveTo(0, height);
        for (let x = 0; x <= width; x++) {
          const y = height - 20 * Math.sin((x / 150) * 2 * Math.PI + time);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(width, height);
        ctx.closePath();
        ctx.fill();

        // 第二条波浪（速度和高度略有不同）
        ctx.fillStyle = 'rgba(0, 150, 230, 0.1)';
        ctx.beginPath();
        ctx.moveTo(0, height);
        for (let x = 0; x <= width; x++) {
          const y = height - 15 * Math.sin((x / 100) * 2 * Math.PI - time * 1.5);
          ctx.lineTo(x, y);
        }
        ctx.lineTo(width, height);
        ctx.closePath();
        ctx.fill();

        time += 0.02;
        requestAnimationFrame(drawWave);
      }

      drawWave();
    }
  }
};
</script>

<style scoped>
.page1-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background: #03044A;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.3);
}

/* 背景canvas定位铺满 */
.background-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

/* 图表都放上层 */
.center-chart,
.floating-chart {
  position: relative;
  z-index: 10;
}

/* 中间图表样式，占满容器 */
.center-chart {
  width: 100%;
  height: 100%;
}

/* 通用悬浮图样式 */
.floating-chart {
  position: absolute;
  width: 28%;
  height: 35%;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 8px;
  backdrop-filter: blur(6px);
}

/* 左边小图位置 */
.floating-chart.left {
  top: 5%;
  left: 2.5%;
}

/* 右边小图位置 */
.floating-chart.right {
  top: 5%;
  right: 2.5%;
}
</style>


<script>
const chart1 = () => import('./components/page4/chart1');
const chart2 = () => import('./components/page4/chart2');
const chart4 = () => import('./components/page4/chart4');
const chart3 = () => import('./components/page4/chart3');
const chart5 = () => import('./components/page4/chart5');
const chart6 = () => import('./components/page4/chart6');
const chart7 = () => import('./components/page4/chart7');
const chart8 = () => import('./components/page4/chart8');
const chart9 = () => import('./components/page4/chart9');
const areaChart = () => import('./components/areaChart');
const pie = () => import('./components/pie')
const worldMap = () => import('./components/page4/worldMap');
const center = () => import('./components/page4/center');
const FishChart = () => import('./components/page4/FishChart');
const FishBoxPlot = () => import('./components/page4/FishBoxPlot');
const FishViolinPlot = () => import('./components/page4/FishViolinPlot');
const ExportFloatWindow = () => import('./components/page4/ExportFloatWindow');
const FishLengthPredictor = () => import('./components/page4/FishLengthPredictor');

export default {
    name: 'page1',
    props: {
        selectRangeDate: Array
    },
    components: {
        FishChart,
        FishBoxPlot,
        FishViolinPlot,
        ExportFloatWindow,  // 注册浮窗组件
        FishLengthPredictor,
        center,// 中心
        chart1, // 面积图
        chart2, // 柱图
        pie, // 饼图
        worldMap, // 世界地图
        chart4, // 圆环
        chart3, // 柱图
        chart5, //折线图
        chart6, // 饼环图
        chart7,// 柱图
        chart8, // 漏斗图
        chart9, //柱图
        areaChart // 面积图
    },
    data() {
        return {

            data1: { // 柱图数据1
                name: '柱图数据1',
                number: '100次',
                data: ["排行1", "排行2", "排行3", "排行4", "排行5"],
                color: '192,35,42',
                value: [60, 50, 40, 30, 20]
            },
            data2: {// 饼图数据1
                title: "饼图数据1分类占比",
                color: '#BE232A',

                data: [
                    {
                        value: 60,
                        name: '分类1',
                        itemStyle: {
                            color: '#a262f2'
                        }

                    },
                    {
                        value: 20,
                        name: '分类2',
                        itemStyle: {
                            color: '#2ca8fe'
                        }
                    },
                    {
                        value: 80,
                        name: '分类3',
                        itemStyle: {
                            color: '#feac2c'
                        }
                    },
                    {
                        value: 40,
                        name: '分类4',
                        itemStyle: {
                            color: '#c0232a'
                        }
                    },
                    {
                        value: 40,
                        name: '分类5',
                        itemStyle: {
                            color: '#2cd9fe'
                        }
                    },
                    {
                        value: 40,
                        name: '分类6',
                        itemStyle: {
                            color: '#ff787e'
                        }
                    },
                    {
                        value: 30,
                        name: '其他',
                        itemStyle: {
                            color: '#252448'
                        }
                    }
                ],
            },
            data3: { // 柱图数据2
                name: '柱图数据2',
                number: '100次',
                data: ["排行1", "排行2", "排行3", "排行4", "排行5"],
                color: '40,112,232',
                value: [6, 5, 4, 3, 2]
            },
            // 饼图数据2
            data4: {
                title: "饼图数据2分类占比",
                color: '#2C7BFE',
                data: [
                    {
                        value: 20,
                        name: '分类1',
                        itemStyle: {
                            color: '#feed2c'
                        }

                    },
                    {
                        value: 20,
                        name: '分类2',
                        itemStyle: {
                            color: '#2ca8fe'
                        }
                    },
                    {
                        value: 40,
                        name: '分类3',
                        itemStyle: {
                            color: '#feac2c'
                        }
                    },
                    {
                        value: 40,
                        name: '分类4',
                        itemStyle: {
                            color: '#2c7bfe'
                        }
                    },
                    {
                        value: 100,
                        name: '其他',
                        itemStyle: {
                            color: '#252448'
                        }
                    }
                ],
            },
            // 环形图数据
            data5: {
                title: '环形图数据1',
                data: [
                    {
                        value: 335,
                        name: '模拟1',
                        itemStyle: {
                            color: '#252448'
                        }
                    },
                    {
                        value: 310,
                        name: '模拟2',
                        itemStyle: {
                            color: '#2ca8fe'
                        }
                    },
                    {
                        value: 234,
                        name: '模拟3',
                        itemStyle: {
                            color: '#feed2c'
                        }
                    },
                    {
                        value: 135,
                        name: '其他',
                        itemStyle: {
                            color: '#2871ea'
                        }
                    },
                    {
                        value: 200,
                        name: '模拟4',
                        itemStyle: {
                            color: '#fe672c'
                        }
                    }
                ]
            },
            // 环形数据2
            data6: {
                title: '环形数据2',
                data: [
                    {
                        value: 335,
                        name: '模拟1',
                        itemStyle: {
                            color: '#69f262'
                        }
                    },
                    {
                        value: 310,
                        name: '模拟2',
                        itemStyle: {
                            color: '#c0232a'
                        }
                    },
                    {
                        value: 234,
                        name: '模拟3',
                        itemStyle: {
                            color: '#2cfcfe'
                        }
                    },
                    {
                        value: 135,
                        name: '其他',
                        itemStyle: {
                            color: '#252448'
                        }
                    },
                    {
                        value: 200,
                        name: '模拟4',
                        itemStyle: {
                            color: '#a262f2'
                        }
                    }
                ]
            },
            // 模块二数据
            data7: {
                title: '标题',
                data: [
                    {
                        value: 70,
                        name: '数据1',
                        itemStyle: {
                            color: '#c0232a'
                        }
                    },
                    {
                        value: 60,
                        name: '数据2',
                        itemStyle: {
                            color: '#2870e8'
                        }
                    },
                ],
                data1: [
                    {
                        value: 40,
                        name: '方式1',
                        itemStyle: {
                            color: '#c0232a'
                        }
                    },
                    {
                        value: 60,
                        name: '方式2',
                        itemStyle: {
                            color: '#2870e8'
                        }
                    },
                ]
            },
            // 模块二数据
            data8: {
                title: '标题',
                data: [
                    {
                        value: 80,
                        name: '数据1',
                        itemStyle: {
                            color: '#c0232a'
                        }
                    },
                    {
                        value: 60,
                        name: '数据2',
                        itemStyle: {
                            color: '#2870e8'
                        }
                    },
                ],
                data1: [
                    {
                        value: 40,
                        name: '方式1',
                        itemStyle: {
                            color: '#c2232a'
                        }
                    },
                    {
                        value: 60,
                        name: '方式2',
                        itemStyle: {
                            color: '#fe672c'
                        }
                    },
                    {
                        value: 40,
                        name: '方式3',
                        itemStyle: {
                            color: '#a262f2'
                        }
                    },
                    {
                        value: 20,
                        name: '方式4',
                        itemStyle: {
                            color: '#2870e8'
                        }
                    },
                    {
                        value: 80,
                        name: '方式5',
                        itemStyle: {
                            color: '#feed2c'
                        }
                    }
                ]
            },
            // 模块三面积图
            configData9: {
                title: '【标题】',
                color: '#75deef',
                name: ['（人）', '（人）'],
                data: [
                    {
                        name: '数据1',
                        color: ['#feed2c', '#353103'],
                        data: [240, 132, 101, 134, 90, 170, 110]
                    },
                    {
                        name: '数据2',
                        color: ['#2871ea', '#0a1b41'],
                        data: [20, 102, 101, 134, 190, 150, 120]
                    },
                    {
                        name: '数据3',
                        color: ['#935adf', '#230f3e'],
                        data: [100, 32, 101, 134, 150, 110, 180]
                    },
                    {
                        name: '数据4',
                        color: ['#e65f2d', '#551f0b'],
                        data: [120, 122, 141, 144, 60, 220, 120]
                    }
                ]
            },
            // 模块三柱图
            colorsData: [
                {
                    itemStyle: {
                        color: "#2c7bfe",

                    },
                    name: '数据1',
                    value: 255
                },
                {
                    itemStyle: {
                        color: "#c2232a",

                    },
                    name: '数据2',
                    value: 212
                },
                {
                    itemStyle: {
                        color: "#feed2c",

                    },
                    name: '数据3',
                    value: 155
                },
                {
                    itemStyle: {
                        color: "#a262f2",

                    },
                    name: '数据4',
                    value: 55
                },
                {
                    itemStyle: {
                        color: "#62d5f2",
                    },
                    name: '数据5',
                    value: 80
                },
                {
                    itemStyle: {
                        color: "#fe672c",
                    },
                    name: '数据6',
                    value: 160
                },
                {
                    itemStyle: {
                        color: "#69f262",
                    },
                    name: '数据7',
                    value: 114
                },
                {
                    itemStyle: {
                        color: "#2ca8fe",
                    },
                    name: '数据8',
                    value: 20
                },
            ],
            resizeFn: null
        }
    },
    methods: {},
    watch: {
        selectRangeDate: function () {
            for (let i = 1; i < 18; i++) {
                this.$refs['chart' + i].setChart();
            }
        }
    },
    mounted() {
        this.resizeFn = this.$debounce(() => {
            // 通过捕获系统的onresize事件触发我们需要执行的事件
            for (let i = 1; i < 18; i++) {
                this.$refs['chart' + i].setChart();
            }
        }, 500)
        window.addEventListener('resize', this.resizeFn)

    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn)
    }

}

</script>

<style lang="less">
.page1 {
    height: 100%;
    width: 100%;
    padding: 14px 20px 20px;
    background: #03044A;
    overflow: hidden;

    .listTop {
        height: 60%;

        .ivu-col {
            height: 100%;

            .leftTop {
                width: 100%;
                height: 100%;
                border: 1px solid #0D2451;
                position: relative;

                .left1 {
                    width: 100%;
                    height: 40%;
                }

                .left2, .left3 {
                    width: 100%;
                    height: 30%;
                    padding: 10px 0;
                }
            }

            .rightTop-1 {
                width: 100%;
                height: 55%;
                border: 1px solid #0D2451;
                position: relative;
            }

            .rightTop-2 {
                width: 100%;
                margin-top: 5%;
                height: 40%;
                border: 1px solid #0D2451;
                position: relative;

                .rightTop-list {
                    width: 100%;
                    height: 100%;

                    .list {
                        width: 30%;
                        height: 100%;
                        float: left;

                        &:first-child {
                            width: 40%;
                        }
                    }
                }
            }

        }
    }

    .listBottom {
        height: 40%;

        .ivu-col-span-9 {
            width: 33.5%;
            margin-right: 0.6667%;
        }

        .ivu-col-span-4 {
            width: 17.66667%;
            margin-right: 0.6667%;
        }

        .ivu-col {
            height: 100%;

            .content {
                margin-top: 30px;
                height: calc(~"100% - 30px");
                border: 1px solid #0D2451;
                position: relative;

                .ivu-row {
                    &.topLine {
                        height: 55%;
                    }

                    &.bottomPie {
                        height: 45%;
                    }

                    .ivu-col {
                        height: 100%;

                        .charts-list {
                            height: 100%;
                            width: 100%;
                        }
                    }
                }

                .behavior {
                    width: 100%;
                    height: 100%;
                }

                .appUse {
                    width: 100%;
                    height: 100%;
                }
            }
        }
    }
}
</style>
