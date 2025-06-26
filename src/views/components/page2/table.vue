<template>
  <div class="leftBar">
    <div class="filters">
      <div>
        <label style="color: white; font-size: 12px;">筛选省份：</label>
        <select v-model="selectedProvince" @change="fetchData">
          <option value="">全部</option>
          <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
        </select>
      </div>
      <div>
        <label style="color: white; font-size: 12px;">筛选流域：</label>
        <select v-model="selectedBasin" @change="fetchData">
          <option value="">全部</option>
          <option v-for="b in basins" :key="b" :value="b">{{ b }}</option>
        </select>
      </div>
      <!-- ✅ 下载按钮 -->
      <div class="download-wrapper">
        <label style="visibility: hidden;">下载</label>
        <button class="download-btn" @click="downloadTable">下载表格</button>
      </div>
    </div>

    <div class="table-wrapper">
      <table class="data-table">
        <thead>
          <tr>
            <th>断面名称</th>
            <th>最新站点情况</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in tableData" :key="row.断面名称">
            <td>{{ row.断面名称 }}</td>
            <td :style="{
              color: row.站点情况 === '正常'
                ? 'limegreen'
                : row.站点情况 === '维护'
                ? 'yellow'
                : 'red'
            }">
              {{ row.站点情况 }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      selectedProvince: '',
      selectedBasin: '',
      provinces: [],
      basins: [],
      tableData: []
    }
  },
  mounted() {
    this.fetchOptions()
    this.fetchData()
  },
  methods: {
    async fetchOptions() {
      const res = await axios.get('http://localhost:5000/api/section_options')
      this.provinces = res.data.省份
      this.basins = res.data.流域
    },
    async fetchData() {
      const res = await axios.get('http://localhost:5000/api/section_status', {
        params: {
          省份: this.selectedProvince,
          流域: this.selectedBasin
        }
      })
      this.tableData = res.data
    },
    // ✅ 下载表格为 CSV 文件
    downloadTable() {
      const headers = ['断面名称', '最新站点情况']
      const rows = this.tableData.map(row => [row.断面名称, row.站点情况])

      let csvContent = '\uFEFF' + headers.join(',') + '\n' +
        rows.map(r => r.map(v => `"${v}"`).join(',')).join('\n')

      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
      const link = document.createElement('a')
      link.href = URL.createObjectURL(blob)
      link.setAttribute('download', '站点状态表.csv')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    }
  }
}
</script>

<style scoped>
.leftBar {
  background: #151456;
  padding: 12px;
  color: white;
  width: 100%;
}
.filters {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 10px;
  align-items: flex-end;
}
.download-wrapper {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
}
.download-btn {
  background: rgba(92, 169, 230, 0.6);
  color: white;
  border: none;
  padding: 6px 10px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.3s ease;
}
.download-btn:hover {
  background: rgba(92, 169, 230, 0.9);
}
.table-wrapper {
  max-height: 170px;
  overflow-y: auto;
}
.data-table {
  width: 100%;
  border-collapse: collapse;
  color: white;
  font-size: 14px;
}
.data-table th,
.data-table td {
  border: 1px solid #444;
  padding: 6px 12px;
  text-align: left;
}
.data-table th {
  background: #1c1c3a;
}
select {
  background: linear-gradient(135deg, #0d1a33, #102040);
  border: 1px solid #00ccff;
  border-radius: 6px;
  padding: 6px 10px;
  color: #63ddff;
  font-size: 8px;
  outline: none;
  box-shadow: 0 0 8px rgba(0, 204, 255, 0.3);
  transition: box-shadow 0.3s ease;
}
select:hover {
  box-shadow: 0 0 12px rgba(0, 204, 255, 0.6);
  border-color: #33ccff;
}
</style>
