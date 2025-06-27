<template>
  <div class="fish-length-predictor">
    <h4>鱼类体长预测</h4>
    <form @submit.prevent="doPredict" class="form">
      <label>
        鱼种
        <select v-model="form.Species" required>
          <option v-for="sp in speciesList" :key="sp" :value="sp">{{ sp }}</option>
        </select>
      </label>
      <label>
        体重 (g)
        <input type="number" v-model.number="form['Weight(g)']" min="0" required />
      </label>
      <label>
        高度 (cm)
        <input type="number" v-model.number="form['Height(cm)']" min="0" step="0.01" required />
      </label>
      <label>
        宽度 (cm)
        <input type="number" v-model.number="form['Width(cm)']" min="0" step="0.01" required />
      </label>
      <button type="submit" :disabled="loading">{{ loading ? '预测中...' : '预测体长' }}</button>
    </form>

    <div v-if="prediction" class="result">
      <h5>预测结果</h5>
      <p>Length1: {{ prediction['Length1(cm)'] }} cm</p>
      <p>Length2: {{ prediction['Length2(cm)'] }} cm</p>
      <p>Length3: {{ prediction['Length3(cm)'] }} cm</p>
    </div>

    <div v-if="errorMsg" class="error">{{ errorMsg }}</div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FishLengthPredictor',
  data() {
    return {
      speciesList: ["Bream", "Roach", "Whitefish", "Parkki", "Perch", "Pike", "Smelt"], // 可以拓展或改为动态载入
      form: {
        Species: "Bream",
        "Weight(g)": null,
        "Height(cm)": null,
        "Width(cm)": null
      },
      prediction: null,
      errorMsg: "",
      loading: false
    };
  },
  methods: {
    async doPredict() {
      this.errorMsg = "";
      this.prediction = null;
      this.loading = true;
      try {
        const res = await axios.post('http://localhost:5000/api/predict_length', this.form);
        if(res.data.error){
          this.errorMsg = res.data.error;
        } else {
          this.prediction = res.data;
        }
      } catch (e) {
        this.errorMsg = "请求失败，请检查后端服务是否正常";
      } finally {
        this.loading = false;
      }
    }
  }
}
</script>

<style scoped>
.fish-length-predictor {
  margin-top: 12px;
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border-radius: 12px;
  color: white;
  font-size: 14px;
}
.form {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
label {
  display: flex;
  flex-direction: column;
  font-weight: 600;
}
input, select {
  margin-top: 6px;
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
}
button:disabled {
  background: rgba(44, 123, 254, 0.5);
  cursor: not-allowed;
}
.result {
  margin-top: 10px;
  background: rgba(0,0,0,0.2);
  padding: 10px;
  border-radius: 6px;
}
.error {
  margin-top: 10px;
  color: #ff6b6b;
}
</style>
