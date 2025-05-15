<template>
    <div class="chart"></div>
</template>

<style lang="less" scoped>
.chart {
    height: 100%;
}
</style>

<script>
export default {
    name: 'Radar',
    props: {
        data: Object
    },
    data() {
        return {
            myChart:null
        }
    },
    methods: {
        setChart() {
            console.log("[Radar] 渲染图表中 ID:", this.id);
            console.log("[Radar] 接收到的数据：", this.data);

            let seriesData = []
            this.data.data.forEach(item => {
                seriesData.push(
                    {
                        value: item.value,
                        name: item.name,
                        symbol: 'none',
                        symbolSize: 5,
                        itemStyle: {
                            color: item.color
                        },
                        lineStyle: {
                            color: item.color,
                            width: 1,
                        },
                        emphasis: {
                            lineStyle: {
                                width: 2
                            }
                        }
                    }
                )
            })
            let option = {
                tooltip: {
                    trigger: 'item',
                    axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                        type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
                    },
                },
                title: {
                    text: this.data.title,
                    top: "5%",
                    left: 'center',
                    textStyle: {
                        color: '#fff',
                        fontSize:12,
                    }
                },
                // legend: {
                //     data: this.data.data.map(item => {
                //         return {name: item.name, icon: 'circle'}
                //     }),
                //     left: "center",
                //     top: this.data.position[1],
                //     itemWidth: 7,
                //     itemHeight: 7,
                //     textStyle: {
                //         color: '#67C3D6',
                //         fontSize: 10
                //     }
                // },
                radar: {
                    indicator: this.data.indicator,
                    center: ['50%', '65%'],
                    radius: "60%",
                    
                    startAngle: 90,
                    splitNumber: 4,
                    shape: 'circle',
                    name: {
                    textStyle: {
                        color: 'rgba(255, 255, 255, 0.6)',
                        fontSize: 8,  // 合理字号
                        fontWeight: 'normal'
                        }
                    },
                    axisNameGap: 3,
                    splitArea: {
                        areaStyle: {
                            color: ['#1166C4',
                                '#0C52A4', '#102F7D',
                                '#13216B'],
                        }
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#163794'
                        }
                    },
                    splitLine: {
                        show: false,
                        lineStyle: {
                            color: '#163794'
                        }
                    }
                },
                series: {
                    name: '雷达图',
                    type: 'radar',
                    emphasis: {
                        // color: 各异,
                        lineStyle: {
                            width: 4
                        }
                    },
                    data: seriesData
                }
            };
            // if (this.id == 'bottom_1_2') {
            //     option.legend.left = '5%';
            // }
            if (!this.myChart) this.myChart = this.$echarts(this.$el);

            this.myChart.clear();
            this.myChart.resize(
                {
                    width: this.$el.offsetWidth,
                    height: this.$el.offsetHeight
                }
            )
            this.myChart.setOption(option);
        }
    },
    mounted() {
        this.setChart();
    },
}
</script>

