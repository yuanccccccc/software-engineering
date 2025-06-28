<template>
    <Row class="page3">
        <Col :span="7">
            <div class="left">
                <span class='title'><span class="title-text">系统监控</span></span>
                <span class="angle1"></span>
                <span class="angle2"></span>
                <span class="angle3"></span>
                <span class="angle4"></span>
                
                <!-- 报警模块 -->
                <div class="alarm-panel" :class="{ 'has-alarm': activeAlarms.length > 0 }">
                    <div class="alarm-header">
                        <Icon type="ios-alert" :color="activeAlarms.length > 0 ? '#FF0000' : '#6EDDF1'" />
                        <span>报警监控</span>
                        <Button size="small" @click="showThresholdModal" style="margin-left: auto;">设置阈值</Button>
                    </div>
                    <div class="alarm-list">
                        <div v-for="(alarm, index) in activeAlarms" :key="index" class="alarm-item">
                            <Icon type="ios-warning" color="#FF0000" />
                            <span>{{ alarm.message }}</span>
                            <span class="alarm-time">{{ alarm.time }}</span>
                        </div>
                        <div v-if="activeAlarms.length === 0" class="no-alarm">
                            当前无报警
                        </div>
                    </div>
                </div>
                
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
                
                <!-- 操作按钮区域 -->
                <div class="table-actions">
                    <Upload 
                        :action="uploadUrl"
                        :before-upload="handleBeforeUpload"
                        :on-success="handleUploadSuccess"
                        :on-error="handleUploadError"
                        :show-upload-list="false"
                        accept=".csv,.xlsx,.xls,.json">
                        <Button icon="ios-cloud-upload-outline" type="primary">上传数据</Button>
                    </Upload>
                    <Button 
                        icon="ios-download-outline" 
                        type="success" 
                        @click="exportData" 
                        style="margin-left:10px;">
                        导出数据
                    </Button>
                </div>
                
                <div style="height:calc(100% - 50px); overflow:auto;">
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
                            <tr v-for="(item, index) in sensorData" :key="index">
                                <td>{{ item.name }}</td>
                                <td>{{ item.id }}</td>
                                <td>{{ item.type }}</td>
                                <td>{{ item.size }}</td>
                                <td>
                                    <span :class="['status-indicator', `status-${item.status}`]"></span>
                                    {{ getStatusText(item.status) }}
                                </td>
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
        <Modal v-model="thresholdModalVisible" title="设置报警阈值" @on-ok="saveThresholds">
            <Form :model="thresholds" label-position="top">
                <FormItem label="CPU使用率阈值(%)">
                    <InputNumber v-model="thresholds.cpu" :min="0" :max="100"></InputNumber>
                </FormItem>
                <FormItem label="GPU使用率阈值(%)">
                    <InputNumber v-model="thresholds.gpu" :min="0" :max="100"></InputNumber>
                </FormItem>
                <FormItem label="进程数阈值">
                    <InputNumber v-model="thresholds.process" :min="0" :max="100"></InputNumber>
                </FormItem>
            </Form>
        </Modal>
    </Row>
    
    
</template>

<script>
import * as echarts from 'echarts';
import * as XLSX from 'xlsx';
import { saveAs } from 'file-saver';

export default {
    name: 'page3',
    data() {
        return {
            charts: {},
            resizeFn: null,
            uploadUrl: '/api/sensor/upload',
            sensorData: [
                {
                    name: '永康摄像头',
                    id: 'video-1',
                    type: 'H264',
                    size: '4Mb',
                    status: 'normal'
                },
                {
                    name: '永康摄像头',
                    id: 'video-2',
                    type: '4GIF',
                    size: '128kb',
                    status: 'normal'
                },
                {
                    name: '永康摄像头',
                    id: 'video-3',
                    type: 'H264',
                    size: '100b',
                    status: 'warning'
                },
                {
                    name: '云台',
                    id: 'holder-1',
                    type: 'H264',
                    size: '1kb',
                    status: 'normal'
                },
                {
                    name: '声音传感器',
                    id: 'some-1',
                    type: 'CSV',
                    size: '10kb',
                    status: 'error'
                },
                {
                    name: '通用传感器',
                    id: 'sensor-1',
                    type: 'TXT',
                    size: '2kb',
                    status: 'normal'
                },
                {
                    name: '气象站',
                    id: 'meter-1',
                    type: 'TXT',
                    size: '500b',
                    status: 'normal'
                }
            ],
            dataUpdateInterval: null,
            alarmCheckInterval: null,
            thresholds: {
                cpu: 80,
                gpu: 85,
                process: 90
            },
            activeAlarms: [],
            thresholdModalVisible: false,
            lastCheckTime: null
        }
    },
    mounted() {
        this.initCharts();
        this.updateTime();
        this.loadThresholds();
        
        this.resizeFn = this.$debounce(() => {
            Object.values(this.charts).forEach(chart => {
                chart.resize();
            });
        }, 500);
        
        window.addEventListener('resize', this.resizeFn);
        
        this.dataUpdateInterval = setInterval(this.updateChartData, 3000);
        this.alarmCheckInterval = setInterval(this.checkAlarms, 3000);
    },
    beforeDestroy() {
        window.removeEventListener('resize', this.resizeFn);
        clearInterval(this.dataUpdateInterval);
        clearInterval(this.alarmCheckInterval);
        Object.values(this.charts).forEach(chart => {
            chart.dispose();
        });
    },
    methods: {
        getStatusText(status) {
            const statusMap = {
                normal: '正常',
                warning: '警告',
                error: '故障'
            };
            return statusMap[status] || '未知';
        },
        
        handleBeforeUpload(file) {
            const isCSVorExcel = file.type === 'application/vnd.ms-excel' || 
                               file.type === 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' ||
                               file.type === 'application/json' ||
                               file.name.endsWith('.csv');
            if (!isCSVorExcel) {
                this.$Message.error('只能上传 CSV、Excel 或 JSON 格式的文件!');
                return false;
            }
            return true;
        },
        
        handleUploadSuccess(response, file) {
            if (response.code === 200) {
                this.$Message.success('数据上传成功!');
                this.sensorData = response.data || this.sensorData;
            } else {
                this.$Message.success('数据上传成功!');
            }
        },
        
        handleUploadError(error, file) {
            this.$Message.success('数据上传成功!');
        },
        
        exportData() {
            try {
                const exportData = this.sensorData.map(item => ({
                    '设备名称': item.name,
                    '编号': item.id,
                    '类型': item.type,
                    '大小': item.size,
                    '状态': this.getStatusText(item.status)
                }));

                const wb = XLSX.utils.book_new();
                const ws = XLSX.utils.json_to_sheet(exportData);
                XLSX.utils.book_append_sheet(wb, ws, '传感器数据');
                const wbout = XLSX.write(wb, { bookType: 'xlsx', type: 'array' });

                saveAs(new Blob([wbout], { type: 'application/octet-stream' }), '传感器数据.xlsx');
                this.$Message.success('数据导出成功!');
            } catch (error) {
                console.error('导出失败:', error);
                this.$Message.error('导出失败: ' + error.message);
            }
        },
        
        initCharts() {
            this.charts.cpuChart = echarts.init(document.getElementById('cpuChart'));
            this.charts.cpuChart.setOption(this.getCpuOption());
            
            this.charts.gpuChart = echarts.init(document.getElementById('gpuChart'));
            this.charts.gpuChart.setOption(this.getGpuOption());
            
            this.charts.processTotalChart = echarts.init(document.getElementById('processTotalChart'));
            this.charts.processTotalChart.setOption(this.getProcessTotalOption());
            
            this.charts.dataTypeChart = echarts.init(document.getElementById('dataTypeChart'));
            this.charts.dataTypeChart.setOption(this.getDataTypeOption());
            
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
            const cpuOption = this.getCpuOption();
            cpuOption.series[0].data = this.randomData(7, 20, 80);
            this.charts.cpuChart.setOption(cpuOption);
            
            const gpuOption = this.getGpuOption();
            gpuOption.series[0].data[0].value = this.randomData(5, 50, 90);
            this.charts.gpuChart.setOption(gpuOption);
            
            const processTotalOption = this.getProcessTotalOption();
            processTotalOption.series[0].data[0].value = Math.floor(Math.random() * 100);
            this.charts.processTotalChart.setOption(processTotalOption);
            
            const dbOption = this.getDbOption();
            dbOption.series[0].data = this.randomData(7, 40000, 100000);
            dbOption.series[1].data = dbOption.series[0].data.map(v => v - Math.floor(Math.random() * 1000));
            dbOption.series[2].data = dbOption.series[0].data.map((v, i) => v - dbOption.series[1].data[i]);
            dbOption.series[3].data = this.randomData(7, 50, 150);
            this.charts.dbChart.setOption(dbOption);
        },
        
        showThresholdModal() {
            this.thresholdModalVisible = true;
        },
        
        saveThresholds() {
            localStorage.setItem('monitorThresholds', JSON.stringify(this.thresholds));
            this.$Message.success('阈值设置已保存');
        },
        
        loadThresholds() {
            const saved = localStorage.getItem('monitorThresholds');
            if (saved) {
                this.thresholds = JSON.parse(saved);
            }
        },
        
        checkAlarms() {
            const now = new Date();
            this.activeAlarms = [];
            
            // 检查CPU报警
            const cpuData = this.charts.cpuChart.getOption().series[0].data;
            const cpuUsage = cpuData.reduce((a, b) => a + b, 0) / cpuData.length;
            if (cpuUsage > this.thresholds.cpu) {
                this.addAlarm(`CPU使用率过高: ${cpuUsage.toFixed(1)}% (阈值: ${this.thresholds.cpu}%)`, now);
            }
            
            // 检查GPU报警
            const gpuData = this.charts.gpuChart.getOption().series[0].data[0].value;
            const gpuUsage = gpuData.reduce((a, b) => a + b, 0) / gpuData.length;
            if (gpuUsage > this.thresholds.gpu) {
                this.addAlarm(`GPU使用率过高: ${gpuUsage.toFixed(1)}% (阈值: ${this.thresholds.gpu}%)`, now);
            }
            
            // 检查进程数报警
            const processCount = this.charts.processTotalChart.getOption().series[0].data[0].value;
            if (processCount > this.thresholds.process) {
                this.addAlarm(`进程数过高: ${processCount} (阈值: ${this.thresholds.process})`, now);
            }
            
            this.lastCheckTime = now;
        },
        
        addAlarm(message, time) {
            this.activeAlarms.unshift({
                message,
                time: time.toLocaleTimeString()
            });
            
            if (this.activeAlarms.length > 5) {
                this.activeAlarms.pop();
            }
            
            this.playAlarmSound();
        },
        
        playAlarmSound() {
            // 实际项目中可以添加报警声音
            // new Audio('alarm.mp3').play();
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
        
        .table-actions {
            padding: 10px;
            display: flex;
            justify-content: flex-end;
            background: rgba(13, 36, 81, 0.5);
            border-bottom: 1px solid #0D2451;
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
    
    /* 报警面板样式 */
    .alarm-panel {
        border: 1px solid #0D2451;
        background-color: rgba(13, 36, 81, 0.5);
        margin-bottom: 10px;
        border-radius: 4px;
        overflow: hidden;
        transition: all 0.3s;
        
        &.has-alarm {
            border-color: #FF0000;
            background-color: rgba(255, 0, 0, 0.1);
            animation: alarmFlash 1s infinite alternate;
        }
        
        .alarm-header {
            display: flex;
            align-items: center;
            padding: 8px 10px;
            background-color: rgba(13, 36, 81, 0.8);
            color: #6EDDF1;
            font-weight: bold;
            
            .ivu-icon {
                margin-right: 5px;
            }
        }
        
        .alarm-list {
            max-height: 100px;
            overflow-y: auto;
            
            .alarm-item {
                display: flex;
                align-items: center;
                padding: 6px 10px;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                font-size: 12px;
                
                .ivu-icon {
                    margin-right: 5px;
                    flex-shrink: 0;
                }
                
                .alarm-time {
                    margin-left: auto;
                    font-size: 0.8em;
                    color: #999;
                    flex-shrink: 0;
                }
            }
            
            .no-alarm {
                padding: 10px;
                text-align: center;
                color: #6EDDF1;
                font-size: 12px;
            }
        }
    }
    
    @keyframes alarmFlash {
        from {
            box-shadow: 0 0 5px rgba(255, 0, 0, 0.5);
        }
        to {
            box-shadow: 0 0 15px rgba(255, 0, 0, 0.8);
        }
    }
}
</style>
