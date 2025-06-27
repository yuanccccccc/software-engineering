<template>
  <div class="export-float-window">
    <h4>导出CSV数据</h4>
    <div class="fields-list">
      <label v-for="field in allFields" :key="field">
        <input type="checkbox" :value="field" v-model="selectedFields" />
        {{ field }}
      </label>
    </div>
    <button 
      :disabled="selectedFields.length === 0 || !fishData.length" 
      @click="exportSelectedFieldsCSV"
    >
      导出CSV
    </button>
    <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  name: "ExportFloatWindow",
  data() {
    return {
      fishData: [],
      allFields: ["Species", "Weight(g)", "Length1(cm)", "Length2(cm)", "Length3(cm)", "Height(cm)", "Width(cm)"],
      selectedFields: ["Weight(g)", "Length1(cm)"],
      errorMsg: "",
    };
  },
  mounted() {
    this.fetchFishData();
  },
  methods: {
    async fetchFishData() {
      try {
        const res = await axios.get('http://localhost:5000/api/fish_data');
        this.fishData = res.data;
        this.errorMsg = '';
      } catch (error) {
        this.errorMsg = "获取数据失败，请检查后端服务";
      }
    },
    exportSelectedFieldsCSV() {
      if (this.selectedFields.length === 0) {
        alert("请选择导出的字段");
        return;
      }
      if (!this.fishData.length) {
        alert("没有可导出的数据");
        return;
      }
      const header = this.selectedFields.join(",") + "\n";
      const csvRows = this.fishData.map(row =>
        this.selectedFields.map(field => {
          let val = row[field];
          if (val === null || val === undefined) val = '';
          if (typeof val === "string" && (val.includes(",") || val.includes("\""))) {
            val = `"${val.replace(/"/g, '""')}"`;
          }
          return val;
        }).join(",")
      );
      const csvContent = header + csvRows.join("\n");
      const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
      const link = document.createElement("a");
      link.href = URL.createObjectURL(blob);
      link.download = "fish_data_selected_fields.csv";
      link.click();
      URL.revokeObjectURL(link.href);
    },
  },
};
</script>

<style scoped>
.export-float-window {
  margin-top: 12px;
  background: rgba(255, 255, 255, 0.05);
  padding: 16px 20px;           /* 增大内边距，让整体更舒展 */
  border-radius: 12px;
  color: white;
  font-size: 16px;              /* 字体放大 */
  user-select: none;
  width: 450px;                 /* 设置更宽一些 */
}
.export-float-window h4 {
  font-weight: 700;
  margin-bottom: 12px;
  font-size: 20px;              /* 标题更大 */
}
.fields-list {
  max-height: 140px;            /* 高度增加方便滚动 */
  overflow-y: auto;
  margin-bottom: 14px;
}
.fields-list label {
  display: block;
  margin-bottom: 6px;
  cursor: pointer;
  font-size: 16px;              /* 复选框标签文字变大 */
}
button {
  padding: 10px 18px;           /* 按钮更大 */
  background: #2c7bfe;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  color: white;
  font-weight: 700;
  font-size: 16px;              /* 按钮字体增大 */
  transition: background-color 0.3s ease;
}
button:disabled {
  background: rgba(44, 123, 254, 0.5);
  cursor: not-allowed;
}
.error-msg {
  margin-top: 10px;
  color: #ff6b6b;
  font-size: 14px;              /* 错误提示字体稍增大 */
}
</style>
