<template>
    <div class="waterDataChart">
        <div class="progress-container" v-for="(item, index) in data" :key="index">
            <div class="progress-title">
                <span class="parameter-name">{{ item.subtitle }}</span>
                <span class="parameter-value">{{ item.data.value }}{{ item.unit || '' }}</span>
            </div>
            <div class="progress-bar-container">
                <div class="progress-bar-bg"></div>
                <div class="progress-bar" :style="{
                    width: calculateWidth(item) + '%',
                    backgroundColor: item.data.color
                }"></div>
            </div>
        </div>
    </div>
</template>

<style lang="less" scoped>
.waterDataChart {
    height: 100%;
    width: 100%;
    padding: 20px 10px 10px;
    display: flex;
    flex-direction: column;
    overflow: auto;
    
    .progress-container {
        margin-bottom: 5px;
        
        .progress-title {
            display: flex;
            justify-content: space-between;
            margin-bottom: 5px;
            
            .parameter-name {
                color: #8CBCCD;
                font-size: 12px;
            }
            
            .parameter-value {
                color: #fff;
                font-size: 12px;
                font-weight: bold;
            }
        }
        
        .progress-bar-container {
            position: relative;
            height: 12px;
            margin: 5px 0;
            
            .progress-bar-bg {
                position: absolute;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: #1F1E4E;
                border-radius: 6px;
            }
            
            .progress-bar {
                position: absolute;
                top: 0;
                left: 0;
                height: 100%;
                border-radius: 6px;
                transition: width 0.5s ease;
            }
        }
    }
}
</style>

<script>
export default {
    props: {
        title: String,
        data: Array,
    },
    name: 'waterDataChart',
    methods: {
        // 计算进度条宽度百分比
        calculateWidth(item) {
            const min = item.min || 0;
            const max = item.max || 100;
            const value = item.data.value;
            
            // 确保值在范围内
            const clampedValue = Math.min(Math.max(value, min), max);
            
            // 计算百分比
            return ((clampedValue - min) / (max - min)) * 100;
        }
    }
}
</script>