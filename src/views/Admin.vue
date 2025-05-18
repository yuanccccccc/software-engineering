<template>
  <div class="admin-container">
    <!-- 左边用户列表 -->
    <div class="user-list">
      <h2>用户列表</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>用户名</th>
            <th>权限</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.role }}</td>
            <td>
              <button class="btn upgrade-btn">提升权限</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 右边部分 -->
    <div class="right-panel">
      <!-- 导航按钮 -->
      <div class="nav-buttons">
        <button class="btn nav-btn">首页</button>
        <button class="btn nav-btn">用户管理</button>
        <button class="btn nav-btn">设置</button>
        <button class="btn nav-btn">日志</button>
      </div>

      <!-- 柱状图 -->
      <div ref="barChart" class="bar-chart"></div>
    </div>
  </div>
</template>

<script>
import * as echarts from "echarts";

export default {
  name: "AdminPage",
  data() {
    return {
      users: [
        { id: 1, name: "alice", role: "普通用户" },
        { id: 2, name: "bob", role: "管理员" },
        { id: 3, name: "carol", role: "普通用户" },
        { id: 4, name: "dave", role: "普通用户" },
        { id: 5, name: "eve", role: "管理员" },
        { id: 6, name: "frank", role: "普通用户" },
        { id: 7, name: "grace", role: "普通用户" },
        { id: 8, name: "heidi", role: "普通用户" },
      ],
      chart: null,
      loginData: [],
    };
  },
  mounted() {
    this.generateRandomLoginData();
    this.initChart();
    window.addEventListener("resize", this.chartResize);
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.chartResize);
    if (this.chart) {
      this.chart.dispose();
    }
  },
  methods: {
    generateRandomLoginData() {
      // 生成过去7天登录人数随机数据
      const today = new Date();
      const dates = [];
      const counts = [];
      for (let i = 6; i >= 0; i--) {
        const d = new Date(today);
        d.setDate(today.getDate() - i);
        const dateStr = d.toISOString().slice(5, 10); // MM-DD 格式
        dates.push(dateStr);
        counts.push(Math.floor(Math.random() * 100) + 20);
      }
      this.loginData = { dates, counts };
    },
    initChart() {
      this.chart = echarts.init(this.$refs.barChart);
      const option = {
        backgroundColor: "transparent",
        title: {
          text: "最近7天登录人数",
          left: "center",
          textStyle: {
            color: "#bcd4ff",
            fontWeight: "normal",
          },
        },
        tooltip: {
          trigger: "axis",
          backgroundColor: "rgba(50,50,50,0.7)",
          textStyle: {
            color: "#fff",
          },
        },
        xAxis: {
          type: "category",
          data: this.loginData.dates,
          axisLine: {
            lineStyle: { color: "#7ea1ff" },
          },
          axisLabel: {
            color: "#bcd4ff",
          },
        },
        yAxis: {
          type: "value",
          axisLine: {
            lineStyle: { color: "#7ea1ff" },
          },
          axisLabel: {
            color: "#bcd4ff",
          },
          splitLine: {
            lineStyle: {
              color: "rgba(255, 255, 255, 0.1)",
            },
          },
        },
        series: [
          {
            data: this.loginData.counts,
            type: "bar",
            barWidth: "40%",
            itemStyle: {
              color: "#409EFF",
            },
          },
        ],
        grid: {
          left: "12%",
          right: "12%",
          bottom: "18%",
          top: "25%",
        },
      };
      this.chart.setOption(option);
    },
    chartResize() {
      if (this.chart) {
        this.chart.resize();
      }
    },
  },
};
</script>

<style scoped>
.admin-container {
  display: flex;
  height: 100vh;
  padding: 20px;
  background: #03044a;
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  gap: 20px;
  color: #bcd4ff;
}

/* 左边列表占50%左右 */
.user-list {
  flex: 1 1 60%;
  background: rgba(6, 15, 78, 0.85);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 0 20px rgba(20, 50, 120, 0.7);
  overflow-y: auto;
}

.user-list h2 {
  margin-bottom: 15px;
  color: #a4c6ff;
}

.user-list table {
  width: 100%;
  border-collapse: collapse;
}

.user-list th,
.user-list td {
  text-align: left;
  padding: 10px;
  border-bottom: 1px solid rgba(170, 190, 255, 0.2);
  font-size: 14px;
  color: #c4d6ff;
}

.user-list th {
  background-color: rgba(10, 30, 90, 0.6);
  color: #8abaff;
  font-weight: 600;
}

.btn {
  padding: 8px 18px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: background-color 0.25s ease;
  user-select: none;
  box-shadow: 0 0 6px rgba(64, 158, 255, 0.7);
}

.upgrade-btn {
  background-color: #409eff;
  color: white;
  font-weight: 600;
}

.upgrade-btn:hover {
  background-color: #66b1ff;
  box-shadow: 0 0 10px rgba(102, 177, 255, 0.9);
}

/* 右边面板 */
.right-panel {
  flex: 1 1 50%;
  display: flex;
  flex-direction: column;
  gap: 30px;
}

/* 上部导航按钮 */
.nav-buttons {
  display: flex;
  gap: 18px;
  justify-content: flex-start;
}

.nav-btn {
  background-color: #52c41a; /* 绿蓝色调更明亮 */
  color: white;
  font-weight: 700;
  padding: 12px 26px;
  font-size: 16px;
  box-shadow: 0 0 12px rgba(82, 196, 26, 0.8);
  transition: background-color 0.3s ease;
  border-radius: 8px;
  user-select: none;
}

.nav-btn:hover {
  background-color: #73d13d;
  box-shadow: 0 0 18px rgba(115, 209, 61, 1);
}

/* 柱状图区域，修改高度比之前小些 */
.bar-chart {
  flex-grow: 1;
  background: rgba(6, 15, 78, 0.7);
  border-radius: 10px;
  box-shadow: 0 0 20px rgba(20, 50, 120, 0.6);
}
</style>
