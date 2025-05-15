<template>
    <div class="chinaMap"></div>
</template>

<script>
import "@/lib/china.js"

export default {
    name: '',
    data() {
        return {
            myChart: null,
            fishingGrounds: [
                { name: '渤海', value: 150, coord: [121.15, 38.55] },
                { name: '黄海', value: 180, coord: [123.5, 35.7] },
                { name: '东海', value: 200, coord: [125.5, 29.5] },
                { name: '南海', value: 220, coord: [114.5, 19.5] }
            ]
        }
    },
    methods: {
        setMap() {
            let option = {
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        if (params.componentSubType === 'effectScatter') {
                            return `${params.name}<br/>经度: ${params.value[0]}<br/>纬度: ${params.value[1]}`;
                        }
                        return params.name;
                    }
                },
                geo: {
                    map: 'china',
                    emphasis: {
                        label: {
                            show: false
                        },
                    },
                    roam: false,
                    itemStyle: {
                        areaColor: '#2043AA',
                        borderColor: '#111'
                    }
                },
                series: [
                    {
                        name: '渔场',
                        type: 'effectScatter',
                        coordinateSystem: 'geo',
                        data: this.fishingGrounds.map(item => {
                            return {
                                name: item.name,
                                value: [item.coord[0], item.coord[1], item.value]
                            };
                        }),
                        symbolSize: function (val) {
                            return val[2] / 10;
                        },
                        showEffectOn: 'render',
                        rippleEffect: {
                            brushType: 'stroke'
                        },
                        emphasis: {
                            scale: true
                        },
                        label: {
                            formatter: '{b}',
                            position: 'right',
                            show: true
                        },
                        itemStyle: {
                            color: function (params) {
                                var colorList = ['#FFA200', '#0006FF', '#D6FC01', '#00D8FF']
                                return colorList[params.dataIndex % 4];
                            },
                            shadowBlur: 10,
                        },
                        zlevel: 1
                    }
                ]
            };
            if (!this.myChart) this.myChart = this.$echarts(this.$el);

            this.myChart.clear();
            this.myChart.resize();
            this.myChart.setOption(option);
            
            // 添加点击事件，显示经纬度信息
            this.myChart.on('click', (params) => {
                if (params.componentSubType === 'effectScatter') {
                    this.$message.info(`${params.name} - 经度: ${params.value[0]}, 纬度: ${params.value[1]}`);
                }
            });
        },
    },
    mounted() {
        this.setMap();
        // 响应窗口大小变化
        window.addEventListener('resize', () => {
            if (this.myChart) {
                this.myChart.resize();
            }
        });
    },
    beforeDestroy() {
        // 移除事件监听
        window.removeEventListener('resize', this.myChart.resize);
        if (this.myChart) {
            this.myChart.dispose();
            this.myChart = null;
        }
    }
}
</script>

<style lang="less" scoped>
.chinaMap {
    height: 100%;
    width: 100%;
}
</style>