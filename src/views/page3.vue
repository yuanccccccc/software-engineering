<template>
    <Row class="page3">
        <Col :span="7">
            <div class="left">
                <span class='title'><span class="title-text">系统监控</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <div class="left1" style="height:60%;">
                    <div style="height:50%;">
                        <div id="cpuChart" style="height:100%;"></div>
                    </div>
                    <div style="height:50%;">
                        <div id="gpuChart" style="height:100%;"></div>
                    </div>
                </div>
                <div class="left1" style="height:40%;">
                    <div id="dataTypeChart" style="height:100%;"></div>
                </div>
            </div>
        </Col>
        <Col :span="10" style="padding:0 1%;">
            <div class="center-top">
                <div id="dbChart" style="height:100%;"></div>
            </div>
            <div class="center-bottom">
                <span class='title'><span class="title-text">设备信息</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                <div style="height:100%; overflow:auto;">
                    <table class="device-table">
                        <thead>
                            <tr>
                                <th>设备名称</th>
                                <th>编号</th>
                                <th>类型</th>
                                <th>大小</th>
                                <th>状态</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>永康摄像头</td>
                                <td>video-1</td>
                                <td>H264</td>
                                <td>4Mb</td>
                                <td><span class="status-indicator status-normal"></span>正常</td>
                            </tr>
                            <tr>
                                <td>永康摄像头</td>
                                <td>video-2</td>
                                <td>4GIF</td>
                                <td>128kb</td>
                                <td><span class="status-indicator status-normal"></span>正常</td>
                            </tr>
                            <tr>
                                <td>永康摄像头</td>
                                <td>video-3</td>
                                <td>H264</td>
                                <td>100b</td>
                                <td><span class="status-indicator status-warning"></span>警告</td>
                            </tr>
                            <tr>
                                <td>云台</td>
                                <td>holder-1</td>
                                <td>H264</td>
                                <td>1kb</td>
                                <td><span class="status-indicator status-normal"></span>正常</td>
                            </tr>
                            <tr>
                                <td>声音传感器</td>
                                <td>some-1</td>
                                <td>CSV</td>
                                <td>10kb</td>
                                <td><span class="status-indicator status-error"></span>故障</td>
                            </tr>
                            <tr>
                                <td>通用传感器</td>
                                <td>sensor-1</td>
                                <td>TXT</td>
                                <td>2kb</td>
                                <td><span class="status-indicator status-normal"></span>正常</td>
                            </tr>
                            <tr>
                                <td>气象站</td>
                                <td>meter-1</td>
                                <td>TXT</td>
                                <td>500b</td>
                                <td><span class="status-indicator status-normal"></span>正常</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </Col>
        <Col :span="7">
            <div class="right-1">
                <div class="right1-1">
                    <span class='title'><span class="title-text">数据中心信息</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <div class="data-center-info">
                        <div class="info-item">
                            <span class="info-label">地点：</span>
                            <span class="info-value">杭州</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">服务器：</span>
                            <span class="info-value">阿里云</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">连接延迟：</span>
                            <span class="info-value">30ms</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">当前时间：</span>
                            <span class="info-value" id="currentTime"></span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">日期：</span>
                            <span class="info-value" id="currentDate"></span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">温度：</span>
                            <span class="info-value">12-14℃</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">平均传输时长：</span>
                            <span class="info-value">02:45</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">平均处理时长：</span>
                            <span class="info-value">00:02</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="right-1" style="height:40%;">
                <div class="right1-1" style="height:100%;">
                    <span class='title'><span class="title-text">进程监控</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <div id="processTotalChart" style="height:100%;"></div>
                </div>
            </div>
            <div class="right-2" style="height:40%;">
                <div class="right1-1" style="height:100%;">
                    <span class='title'><span class="title-text">数据库统计</span></span>
                    <span class="angle1"></span>
                    <span class="angle2"></span>
                    <span class="angle3"></span>
                    <span class="angle4"></span>
                    <div style="padding:10px;">
                        <div class="info-item">
                            <span class="info-label">数据来源：</span>
                            <span class="info-value">MySQL，HBase</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">查询次数：</span>
                            <span class="info-value">567,890</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">成功次数：</span>
                            <span class="info-value">567,890</span>
                        </div>
                        <div class="info-item">
                            <span class="info-label">查询时间：</span>
                            <span class="info-value">0.1s</span>
                        </div>
                    </div>
                </div>
            </div>
        </Col>
    </Row>
</template>

<script>
import * as echarts from 'echarts';

export default {
    name: 'page3',
    data() {
        return {
            charts: {},
            resizeFn: null
        }
    },
    mounted() {
        this.initCharts();
        this.updateTime();
        
        this.resizeFn = this.$debounce(() => {
            Object.values(this.charts).forEach(chart => {
                chart.resize();
            });
        }, 500);
        
        window.addEventListener('resize', this.resizeFn);
        
        // 定时更新数据
        this.dataUpdateInterval = setInterval(this.updateChartData, 3000);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn);
        clearInterval(this.dataUpdateInterval);
        Object.values(this.charts).forEach(chart => {
            chart.dispose();
        });
    },
    methods: {
        initCharts() {
            // 1. CPU运行状态图表
            this.charts.cpuChart = echarts.init(document.getElementById('cpuChart'));
            this.charts.cpuChart.setOption(this.getCpuOption());
            
            // 2. GPU运行状态图表
            this.charts.gpuChart = echarts.init(document.getElementById('gpuChart'));
            this.charts.gpuChart.setOption(this.getGpuOption());
            
            // 3. 进程总量图表
            this.charts.processTotalChart = echarts.init(document.getElementById('processTotalChart'));
            this.charts.processTotalChart.setOption(this.getProcessTotalOption());
            
            // 4. 数据类型统计图表
            this.charts.dataTypeChart = echarts.init(document.getElementById('dataTypeChart'));
            this.charts.dataTypeChart.setOption(this.getDataTypeOption());
            
            // 5. 数据库交互统计图表
            this.charts.dbChart = echarts.init(document.getElementById('dbChart'));
            this.charts.dbChart.setOption(this.getDbOption());
        },
        updateTime() {
            const now = new Date();
            document.getElementById('currentTime').textContent = now.toLocaleTimeString();
            document.getElementById('currentDate').textContent = now.toLocaleDateString();
            setTimeout(this.updateTime, 1000);
        },
        randomData(count, min, max) {
            const data = [];
            for (let i = 0; i < count; i++) {
                data.push(Math.floor(Math.random() * (max - min + 1)) + min);
            }
            return data;
        },
        updateChartData() {
            // 更新CPU数据
            const cpuOption = this.getCpuOption();
            cpuOption.series[0].data = this.randomData(7, 20, 80);
            this.charts.cpuChart.setOption(cpuOption);
            
            // 更新GPU数据
            const gpuOption = this.getGpuOption();
            gpuOption.series[0].data[0].value = this.randomData(5, 50, 90);
            this.charts.gpuChart.setOption(gpuOption);
            
            // 更新进程总量
            const processTotalOption = this.getProcessTotalOption();
            processTotalOption.series[0].data[0].value = Math.floor(Math.random() * 100);
            this.charts.processTotalChart.setOption(processTotalOption);
            
            // 更新数据库数据
            const dbOption = this.getDbOption();
            dbOption.series[0].data = this.randomData(7, 40000, 100000);
            dbOption.series[1].data = dbOption.series[0].data.map(v => v - Math.floor(Math.random() * 1000));
            dbOption.series[2].data = dbOption.series[0].data.map((v, i) => v - dbOption.series[1].data[i]);
            dbOption.series[3].data = this.randomData(7, 50, 150);
            this.charts.dbChart.setOption(dbOption);
        },
        getCpuOption() {
            return {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        label: {
                            backgroundColor: '#6a7985'
                        }
                    }
                },
                title: {
                    text: 'CPU利用率',
                    left: 'center',
                    textStyle: {
                        color: '#6EDDF1'
                    }
                },
                xAxis: {
                    type: 'category',
                    boundaryGap: false,
                    data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                    axisLine: {
                        lineStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    axisLabel: {
                        color: '#6EDDF1'
                    }
                },
                yAxis: {
                    type: 'value',
                    min: 0,
                    max: 100,
                    axisLabel: {
                        formatter: '{value}%',
                        color: '#6EDDF1'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(110, 221, 241, 0.2)'
                        }
                    }
                },
                series: [{
                    name: 'CPU使用率',
                    type: 'line',
                    smooth: true,
                    lineStyle: {
                        width: 0
                    },
                    showSymbol: false,
                    areaStyle: {
                        opacity: 0.8,
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{
                            offset: 0,
                            color: 'rgba(58, 77, 233, 0.8)'
                        }, {
                            offset: 1,
                            color: 'rgba(58, 77, 233, 0.1)'
                        }])
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    data: this.randomData(7, 20, 80)
                }]
            };
        },
        getGpuOption() {
            return {
                title: {
                    text: 'GPU利用率',
                    left: 'center',
                    textStyle: {
                        color: '#6EDDF1'
                    }
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'shadow'
                    }
                },
                radar: {
                    indicator: [
                        { name: '计算', max: 100 },
                        { name: '显存', max: 100 },
                        { name: '温度', max: 100 },
                        { name: '功耗', max: 100 },
                        { name: '带宽', max: 100 }
                    ],
                    name: {
                        textStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(110, 221, 241, 0.5)'
                        }
                    },
                    splitArea: {
                        show: false
                    },
                    axisLine: {
                        lineStyle: {
                            color: 'rgba(110, 221, 241, 0.5)'
                        }
                    }
                },
                series: [{
                    name: 'GPU状态',
                    type: 'radar',
                    data: [{
                        value: [80, 65, 70, 60, 75],
                        name: '当前状态',
                        areaStyle: {
                            color: 'rgba(0, 204, 255, 0.4)'
                        },
                        lineStyle: {
                            width: 2,
                            color: '#00CCFF'
                        },
                        itemStyle: {
                            color: '#00CCFF'
                        }
                    }]
                }]
            };
        },
        getProcessTotalOption() {
            return {
                series: [{
                    type: 'gauge',
                    center: ['50%', '60%'],
                    startAngle: 180,
                    endAngle: 0,
                    min: 0,
                    max: 100,
                    splitNumber: 10,
                    axisLine: {
                        lineStyle: {
                            width: 30,
                            color: [
                                [0.3, '#67e0e3'],
                                [0.7, '#37a2da'],
                                [1, '#fd666d']
                            ]
                        }
                    },
                    pointer: {
                        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
                        length: '12%',
                        width: 20,
                        offsetCenter: [0, '-60%'],
                        itemStyle: {
                            color: 'auto'
                        }
                    },
                    axisTick: {
                        length: 12,
                        lineStyle: {
                            color: 'auto',
                            width: 2
                        }
                    },
                    splitLine: {
                        length: 20,
                        lineStyle: {
                            color: 'auto',
                            width: 5
                        }
                    },
                    axisLabel: {
                        color: '#6EDDF1',
                        fontSize: 12,
                        distance: -60,
                        formatter: function(value) {
                            if (value === 100) {
                                return '100';
                            }
                            return '';
                        }
                    },
                    detail: {
                        fontSize: 30,
                        offsetCenter: [0, '0%'],
                        valueAnimation: true,
                        formatter: '{value}',
                        color: '#6EDDF1'
                    },
                    data: [{
                        value: Math.floor(Math.random() * 100)
                    }]
                }]
            };
        },
        getDataTypeOption() {
            return {
                tooltip: {
                    trigger: 'item',
                    formatter: '{a} <br/>{b}: {c} ({d}%)'
                },
                legend: {
                    orient: 'vertical',
                    left: 10,
                    data: ['视频数据', '图像数据', '文本数据', '传感器数据', '日志数据'],
                    textStyle: {
                        color: '#6EDDF1'
                    }
                },
                series: [{
                    name: '数据类型',
                    type: 'pie',
                    radius: ['50%', '70%'],
                    avoidLabelOverlap: false,
                    itemStyle: {
                        borderRadius: 10,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        label: {
                            show: true,
                            fontSize: '18',
                            fontWeight: 'bold',
                            color: '#fff'
                        }
                    },
                    labelLine: {
                        show: false
                    },
                    data: [{
                        value: 45,
                        name: '视频数据'
                    }, {
                        value: 20,
                        name: '图像数据'
                    }, {
                        value: 15,
                        name: '文本数据'
                    }, {
                        value: 12,
                        name: '传感器数据'
                    }, {
                        value: 8,
                        name: '日志数据'
                    }]
                }]
            };
        },
        getDbOption() {
            return {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross',
                        crossStyle: {
                            color: '#999'
                        }
                    }
                },
                legend: {
                    data: ['查询次数', '成功次数', '失败次数'],
                    textStyle: {
                        color: '#6EDDF1'
                    }
                },
                xAxis: [{
                    type: 'category',
                    data: ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00', '24:00'],
                    axisPointer: {
                        type: 'shadow'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    axisLabel: {
                        color: '#6EDDF1'
                    }
                }],
                yAxis: [{
                    type: 'value',
                    name: '次数',
                    min: 0,
                    max: 100000,
                    interval: 20000,
                    axisLabel: {
                        formatter: '{value}',
                        color: '#6EDDF1'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    splitLine: {
                        lineStyle: {
                            color: 'rgba(110, 221, 241, 0.2)'
                        }
                    }
                }, {
                    type: 'value',
                    name: '时间(ms)',
                    min: 0,
                    max: 500,
                    interval: 100,
                    axisLabel: {
                        formatter: '{value}',
                        color: '#6EDDF1'
                    },
                    axisLine: {
                        lineStyle: {
                            color: '#6EDDF1'
                        }
                    },
                    splitLine: {
                        show: false
                    }
                }],
                series: [{
                    name: '查询次数',
                    type: 'bar',
                    data: [50000, 70000, 90000, 85000, 95000, 80000, 60000]
                }, {
                    name: '成功次数',
                    type: 'bar',
                    data: [49000, 69500, 89500, 84500, 94500, 79500, 59500]
                }, {
                    name: '失败次数',
                    type: 'bar',
                    data: [1000, 500, 500, 500, 500, 500, 500]
                }, {
                    name: '查询时间',
                    type: 'line',
                    yAxisIndex: 1,
                    data: [120, 90, 80, 70, 60, 80, 100]
                }]
            };
        }
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

        .data-center-info {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-gap: 10px;
            padding: 15px;
            
            .info-item {
                margin-bottom: 8px;
                
                .info-label {
                    font-weight: bold;
                    color: #6EDDF1;
                }
                
                .info-value {
                    color: #fff;
                }
            }
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
        
        .device-table {
            width: 100%;
            border-collapse: collapse;
            color: #fff;
            
            th, td {
                border: 1px solid #0D2451;
                padding: 8px;
                text-align: left;
            }
            
            th {
                background-color: #0D2451;
            }
            
            .status-indicator {
                display: inline-block;
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 5px;
            }
            
            .status-normal {
                background-color: #52c41a;
            }
            
            .status-warning {
                background-color: #faad14;
            }
            
            .status-error {
                background-color: #f5222d;
            }
        }
    }

    .center-top {
        height: 60%;
    }

    .center-bottom {
        height: 40%;
    }

    .right-1 {
        height: 30%;

        .right1-1 {
            height: 92%;
        }
    }

    .right-2 {
        height: 30%;
    }
}
</style>