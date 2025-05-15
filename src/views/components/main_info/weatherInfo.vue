<template>
    <div class="weather-info">
        <!-- 当前天气 -->
        <div class="current-weather">
            <div class="weather-main">
                <div>{{ city }}</div>
                <div>{{ forecastList[0].tem2 }}℃/{{ forecastList[0].tem1 }}℃</div>
                <div>{{ wea }}</div>
            </div>
            <div class="weather-details">
                <div>风力:  {{ win_speed }}</div>
                <div>空气质量:  {{ air_level }}</div>
                <div>日出日落:  {{ sunrise }} ~ {{ sunset }}</div>
                <div>月相:  {{ moonPhrase }}</div>
                <div>降水概率:  {{ rain }}%</div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios";

export default {
    name: 'WeatherInfo',
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
            sunrise: "",
            sunset: "",
            rain: "",
            moonPhrase: "",
            forecastList: []
        }
    },
    methods: {
        get(sky) {
            return "https://xintai.xianguomall.com/skin/pitaya/" + sky + ".png";
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
                    that.sunrise = data.data[0].sunrise;
                    that.sunset = data.data[0].sunset;
                    that.rain = data.data[0].rain;
                    that.moonPhrase = data.data[0].moonPhrase;

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
        }
    },
    mounted() {
        this.fetchWeatherData();
    }
}
</script>

<style lang="less" scoped>
.weather-info {
    height: 100%;
    color: #fff;
    display: flex;
    flex-direction: column;
    padding: 10px;
    
    .current-weather {
        flex: 1;
        display: flex;
        flex-direction: column;
        
        
        .weather-main {
            display: flex;
            align-items: center;
            justify-content: space-around;
            margin: 15px 0;
            font-size: 18px;
            font-weight: bold;
            color: #8CBCCD;
        }
        
        .weather-details {
            align-items: center;
            margin: 0 8px 0;
            font-size: 12px;
            line-height: 1.8;
            // font-weight: bold;
            color: #fff;
        }
    }
    
}
</style>