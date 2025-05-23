import Vue from "vue";
import App from "./App";
import router from "./router";
import iView from "iview";
import "./assets/less/index.less";
import * as echarts from "echarts";
import img from "./lib/img";
import utils from "./lib/utils";

import videojs from "video.js";
import "video.js/dist/video-js.css";
import flvjs from "flv.js";

// // 注册flv插件
// videojs.registerPlugin('flvjs', flvjs);

Vue.prototype.$echarts = function (el) {
  return echarts.init(el, null, { renderer: "svg" });
};
Vue.prototype.$images = img;
Vue.config.productionTip = false;
Vue.use(iView);
Vue.use(utils);
new Vue({
  router,
  render: (h) => h(App),
}).$mount("#app");
