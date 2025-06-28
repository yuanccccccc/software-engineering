<template>
  <div class="fish-length-predictor">
    <h4>鱼类体长预测</h4>
    <form @submit.prevent="doPredict" class="form">
      <label>
        鱼种
        <select v-model="form.Species" required>
          <option v-for="sp in speciesList" :key="sp" :value="sp">
            {{ sp }}
          </option>
        </select>
      </label>
      <label>
        体重 (g)
        <input
          type="number"
          v-model.number="form['Weight(g)']"
          min="0"
          required
        />
      </label>
      <label>
        高度 (cm)
        <input
          type="number"
          v-model.number="form['Height(cm)']"
          min="0"
          step="0.01"
          required
        />
      </label>
      <label>
        宽度 (cm)
        <input
          type="number"
          v-model.number="form['Width(cm)']"
          min="0"
          step="0.01"
          required
        />
      </label>
      <button type="submit" :disabled="loading">
        {{ loading ? "预测中..." : "预测体长" }}
      </button>
    </form>

    <div v-if="errorMsg" class="error">{{ errorMsg }}</div>

    <!-- 弹窗：预测结果 -->
    <div v-if="showResultModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h5>预测结果</h5>
        <p>Length1: {{ prediction["Length1(cm)"] }} cm</p>
        <p>Length2: {{ prediction["Length2(cm)"] }} cm</p>
        <p>Length3: {{ prediction["Length3(cm)"] }} cm</p>
        <button @click="closeModal">关闭</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
export default {
  name: "FishLengthPredictor",
  data() {
    return {
      speciesList: [
        "Bream",
        "Roach",
        "Whitefish",
        "Parkki",
        "Perch",
        "Pike",
        "Smelt",
      ],
      form: {
        Species: "Bream",
        "Weight(g)": null,
        "Height(cm)": null,
        "Width(cm)": null,
      },
      prediction: null,
      errorMsg: "",
      loading: false,
      showResultModal: false, // 新增 控制弹窗显示
    };
  },
  methods: {
    async doPredict() {
      this.errorMsg = "";
      this.prediction = null;
      this.loading = true;
      this.showResultModal = false; // 发送请求前关闭弹窗
      try {
        const res = await axios.post(
          "http://localhost:5000/api/predict_length",
          this.form
        );
        if (res.data.error) {
          this.errorMsg = res.data.error;
        } else {
          this.prediction = res.data;
          this.showResultModal = true; // 请求成功后打开弹窗显示结果
        }
      } catch (e) {
        this.errorMsg = "请求失败，请检查后端服务是否正常";
      } finally {
        this.loading = false;
      }
    },
    closeModal() {
      this.showResultModal = false;
    },
  },
};
</script>

<style scoped>
.fish-length-predictor {
  margin-top: 8px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  color: white;
  font-size: 12px; /* font-size调大点，更合适 */
}
.form {
  display: flex;
  flex-direction: column;
  gap: 6px; /* 控制上下间距 */
}
label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
}
input,
select {
  margin-top: 4px;
  border-radius: 4px;
  border: 1px solid #999;
  padding: 6px 8px;
  font-size: 14px;
}
button {
  padding: 8px 14px;
  background: #2c7bfe;
  color: white;
  font-weight: bold;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
}
button:disabled {
  background: rgba(44, 123, 254, 0.5);
  cursor: not-allowed;
}
.error {
  margin-top: 10px;
  color: #ff6b6b;
}

/* 弹窗遮罩层 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw; /* 视口宽度 */
  height: 100vh; /* 视口高度 */
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999; /* 置顶 */
}

/* 弹窗内容容器 */
.modal-content {
  background: #222;
  color: white;
  padding: 20px 30px;
  border-radius: 8px;
  width: 320px;
  max-width: 90%;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.7);
  text-align: center;
}

.modal-content h5 {
  margin-top: 0;
  margin-bottom: 15px;
}

.modal-content button {
  margin-top: 15px;
  padding: 8px 20px;
  background: #2c7bfe;
  border: none;
  border-radius: 6px;
  color: white;
  cursor: pointer;
  font-weight: 600;
  font-size: 14px;
  transition: background-color 0.3s ease;
}
.modal-content button:hover {
  background: #1b5edb;
}
</style>
