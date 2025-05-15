<template>
<div class="forecast">

    <div class="forecast-list">
    <div class="forecast-item" v-for="(item, index) in forecastList" :key="index">
        <div class="forecast-day">{{ item.day }}</div>
        <div>
            <img 
                :src="getWeatherIcon(item.wea_img)" 
                :alt="item.wea_img"
                @error="handleImageError"
                width="35" 
                height="35"
            >
        </div>
        <div class="forecast-temp">{{ item.tem2 }}℃/{{ item.tem1 }}℃</div>
    </div>
    </div>

    <div class="temperature-trend">
      <div class="trend-container">
        <!-- 最高温折线 -->
        <svg class="trend-line high" viewBox="0 0 100 50" preserveAspectRatio="none">
          <path :d="highTempPath" fill="none" stroke="#ff7e7e" stroke-width="2" />
        </svg>
        
        <!-- 最低温折线 -->
        <svg class="trend-line low" viewBox="0 0 100 50" preserveAspectRatio="none">
          <path :d="lowTempPath" fill="none" stroke="#7eb8ff" stroke-width="2" />
        </svg>
        
        <!-- 数据点标记 -->
        <div 
          v-for="(item, index) in forecastList" 
          :key="'high-'+index"
          class="data-point high"
          :style="getHighTempStyle(index)"
        ></div>
        
        <div 
          v-for="(item, index) in forecastList" 
          :key="'low-'+index"
          class="data-point low"
          :style="getLowTempStyle(index)"
        ></div>
      </div>
    </div>

</div>
</template>

<script>
import axios from "axios";

export default {
    name: 'WeatherForecast',
    data() {
        return {
            city: "",
            update_time: "",
            wea: "",
            tem: "",
            win_speed: "",
            win: "",
            air_level: "",
            air_tips: "",
            wea_img: "",
            forecastList: []
        }
    },
    computed: {
        // 计算最高温折线路径
        highTempPath() {
            return this.calculatePath(this.forecastList.map(item => item.tem1));
        },
        // 计算最低温折线路径
        lowTempPath() {
            return this.calculatePath(this.forecastList.map(item => item.tem2));
        },
        // 计算温度范围用于归一化
        tempRange() {
            const temps = this.forecastList.flatMap(item => [item.tem1, item.tem2]);
            return {
            min: Math.min(...temps),
            max: Math.max(...temps)
            };
        }
    },
    methods: {
        getWeatherIcon(name) {
            const icon = name.toLowerCase();
            try {
                return require(`@/assets/images/weather/${icon}.png`);
            } catch {
                return require('@/assets/images/weather/default.png');
            }
        },
        handleImageError(e) {
            e.target.src = require('@/assets/images/weather/default.png');
        },
        fetchWeatherData() {
            const that = this;
            axios
                .get(
                    "http://gfeljm.tianqiapi.com/api?unescape=1&version=v91&appid=22668659&appsecret=WdFi4vMm&ext=&city=天津"
                )
                .then(function (response) {
                    const data = response.data;
                    that.city = data.city;
                    that.update_time = data.update_time;
                    that.wea = data.data[0].wea;
                    that.tem = data.data[0].tem;
                    that.win_speed = data.data[0].win_speed;
                    that.win = data.data[0].win;
                    that.air_level = data.data[0].air_level;
                    that.air_tips = data.data[0].air_tips;
                    that.wea_img = data.data[0].wea_img;
                    
                    that.forecastList = data.data.slice(1, 6).map(item => {
                        return {
                            day: item.day,
                            wea_img: item.wea_img,
                            tem1: item.tem1,
                            tem2: item.tem2
                        };
                    });
                })
                .catch(function (error) {
                    console.log("请求失败", error);
                });
        },
        calculatePath(temperatures) {
            if (!temperatures || temperatures.length < 2) return '';
            
            const { min, max } = this.tempRange;
            const range = max - min || 1; // 避免除以0
            const points = temperatures.map((temp, i) => {
                const x = (i / (temperatures.length - 1)) * 100;
                const y = 50 - ((temp - min) / range) * 40; // 保留10px边距
                return `${x},${y}`;
            });
            
            return `M${points.join(' L')}`;
        },
        // 获取最高温数据点样式
        getHighTempStyle(index) {
            const temp = this.forecastList[index].tem1;
            const y = 50 - ((temp - this.tempRange.min) / (this.tempRange.max - this.tempRange.min || 1)) * 40;
            return {
                left: `${(index / (this.forecastList.length - 1)) * 100}%`,
                top: `${y}px`,
                backgroundColor: '#ff7e7e'
            };
        },
        
        // 获取最低温数据点样式
        getLowTempStyle(index) {
            const temp = this.forecastList[index].tem2;
            const y = 50 - ((temp - this.tempRange.min) / (this.tempRange.max - this.tempRange.min || 1)) * 40;
            return {
                left: `${(index / (this.forecastList.length - 1)) * 100}%`,
                top: `${y}px`,
                backgroundColor: '#7eb8ff'
            };
        }
    },
    mounted() {
        this.fetchWeatherData();
    }
}
</script>

<style lang="less" scoped>
.forecast {
    height: 100%;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 10px;
        
    .forecast-list {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        margin-top: 15px;
        align-items: center;
        padding-top: 10px;
        // border-top: 1px solid rgba(13, 245, 248, 0.3);
        
        .forecast-item {
            text-align: center;
            font-size: 12px;
            flex-direction: column;
            
            .forecast-day {
                color: #8CBCCD;
                margin-bottom: 5px;
            }
            
            .forecast-temp {
                margin-top: 5px;
                white-space: nowrap;
            }
        }
    }

    .temperature-trend {
        margin-top: 15px;
        margin-bottom: 5px;
        height: 100px;
        position: relative;

        .trend-container {
            width: 100%;
            height: 100%;
            position: relative;
        
            svg {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            }
        
            .data-point {
                position: absolute;
                width: 6px;
                height: 6px;
                border-radius: 50%;
                transform: translate(-50%, -50%);
            
                &.high {
                background-color: #ff7e7e;
                }
                
                &.low {
                background-color: #7eb8ff;
                }
            }
        }
    }
}


</style>