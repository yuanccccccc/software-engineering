
<template>
<div class="device-info">

    <div class="mytips">
      <p><span class="lable">最后更新时间：</span> {{ update_time }}</p>
    </div>

    <div class="content">
        <p><span class="lable">在线设备数：</span><span class="value">{{ o_d_c }} / 10000</span></p>
        <p><span class="lable">设备温度: </span><span class="value">{{ d_t.toFixed(1) }}℃</span></p>
    </div>

    <div class="alarm">
        <p>气象预警：</p>
        <ul v-if="alarms.length > 0">
            <li v-for="(alarm, index) in alarms" :key="index">{{ alarm.alarm_content }}</li>
        </ul>
        <p v-else style="margin-left: 20px;color: #fff;">暂无气象预警</p>
    </div>

</div>
</template>

<script>
import axios from "axios";

export default {
    name: 'device-info',
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
            forecastList: [],
            alarms: [],
            o_d_c: 10000,
            d_t: 35,
            refreshinterval: null
        }
    },
    methods: {
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

                    that.alarms = data.data[0].alarm || [];
                    
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
        simulateDeviceData() {
            // 模拟在线设备数变化 (99%在线率)
            const fluctuation = Math.floor(Math.random() * 41) - 20; // -20到+20的随机波动
            this.o_d_c = Math.min(10000, Math.max(9700, this.o_d_c + fluctuation));
            
            // 模拟温度变化 (20-50℃范围内，每次变化不超过7%)
            const maxChange = this.d_t * 0.07; // 最大变化量
            const tempChange = (Math.random() * 2 - 1) * maxChange; // -7%到+7%
            this.d_t = Math.min(50, Math.max(20, this.d_t + tempChange));
        }
    },
    mounted() {
        this.fetchWeatherData();
        this.refreshInterval = setInterval(() => {
            // this.fetchWeatherData();
            this.simulateDeviceData();
        }, 60000); // 60000毫秒 = 1分钟
        
        // 初始模拟数据
        this.simulateDeviceData();
    },
    beforeDestroy() {
        clearInterval(this.refreshInterval);
    }
}
</script>

<style lang="less" scoped>
.device-info {
    height: 100%;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 10px;
    margin-left: 8px;

    .mytips {
        align-items: center;
        margin: 20px 8px 10px;
        font-size: 12px;
        line-height: 1.8;
        color: #8CBCCD;
        .lable{
            font-weight: bold;
        }

    }

     .alarm {
        align-items: center;
        margin: 15px 8px 0;
        color: #db1010;
        line-height: 1.8;
        
        ul {
            padding-left: 20px;
            margin: 5px 0;
            
            li {
                margin-bottom: 5px;
                font-size: 14px;
            }
        }
    }

    .content {
        line-height: 1.8;
        color: #8CBCCD;
        align-items: center;
        margin: 5px 8px 0;

        .lable {
            color: #8CBCCD;
            font-weight: bold;
        }
        .value {
            color: #fff;
        }

    }
}


</style>