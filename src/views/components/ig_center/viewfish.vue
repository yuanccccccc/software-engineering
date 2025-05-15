<template>
  <div class="viewfish-container">
    <div v-if="isLoading" class="loading">数据加载中...</div>
    <div v-else-if="error" class="error">加载错误: {{ error }}</div>
    <div v-else>
      <div class="header">
        <div class="header-item">帧 ID</div>
        <div class="header-item">鱼类 ID</div>
        <div class="header-item">种类 ID</div>
        <div class="header-item">位置 (x,y)</div>
        <div class="header-item">大小 (w,h)</div>
        <div class="header-item">识别置信度</div>
      </div>
      <div class="fish-data-container" ref="scrollContainer">
        <div 
          v-for="(detection, index) in visibleDetections" 
          :key="index" 
          class="fish-data-row"
          :class="{ 'highlight': detection.highlight }"
        >
          <div class="data-item">{{ detection.frame_id }}</div>
          <div class="data-item">{{ detection.fish_id }}</div>
          <div class="data-item">
            <span :class="'fish-species-' + detection.specie_id">{{ detection.specie_id }}</span>
          </div>
          <div class="data-item">({{ detection.bounding_box_x }}, {{ detection.bounding_box_y }})</div>
          <div class="data-item">({{ detection.bounding_box_w }}, {{ detection.bounding_box_h }})</div>
          <div class="data-item">{{ (detection.rec_certainty >= 0 ? detection.rec_certainty : detection.det_certainty).toFixed(2) }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse';

export default {
  name: 'ViewFish',
  data() {
    return {
      fishDetections: [],
      visibleDetections: [],
      currentIndex: 0,
      scrollInterval: null,
      isLoading: false,
      error: null,
      headers: [
        'detection_id', 'detection_component_id', 'recognition_component_id', 
        'fish_id', 'video_id', 'frame_id', 'bounding_box_x', 'bounding_box_y', 
        'bounding_box_w', 'bounding_box_h', 'specie_id', 'det_certainty', 
        'track_certainty', 'rec_certainty', 'contour'
      ]
    };
  },
  mounted() {
    this.loadCSVData();
  },
  beforeDestroy() {
    if (this.scrollInterval) {
      clearInterval(this.scrollInterval);
    }
  },
  methods: {
    async loadCSVData() {
      this.isLoading = true;
      this.error = null;
      
      try {
        // 使用 fetch API 获取 CSV 文件
        const response = await fetch('/fish_video_data.csv');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const csvText = await response.text();
        
        // 使用Papa解析CSV数据
        const parsedData = Papa.parse(csvText, {
          header: true,
          skipEmptyLines: true,
          dynamicTyping: true,
          transformHeader: header => header.trim()
        });
        
        // 处理解析后的数据
        if (parsedData.data && parsedData.data.length > 0) {
          this.fishDetections = parsedData.data.map(row => ({
            detection_id: row.detection_id,
            detection_component_id: row.detection_component_id,
            recognition_component_id: row.recognition_component_id,
            fish_id: row.fish_id,
            video_id: row.video_id,
            frame_id: row.frame_id,
            bounding_box_x: row.bounding_box_x,
            bounding_box_y: row.bounding_box_y,
            bounding_box_w: row.bounding_box_w,
            bounding_box_h: row.bounding_box_h,
            specie_id: row.specie_id,
            det_certainty: row.det_certainty,
            track_certainty: row.track_certainty,
            rec_certainty: row.rec_certainty,
            contour: row.contour,
            highlight: false
          }));
          
          console.log('成功加载鱼类数据，条目数:', this.fishDetections.length);
          
          this.initVisibleData();
          this.startScrolling();
        } else {
          throw new Error('CSV数据解析出错或为空');
        }
      } catch (error) {
        console.error('加载CSV数据时出错:', error);
        this.error = error.message;
        // 可以在这里添加重试逻辑
      } finally {
        this.isLoading = false;
      }
    },
    
    initVisibleData() {
      const initialCount = 10;
      this.visibleDetections = this.fishDetections.slice(0, initialCount);
      this.currentIndex = initialCount;
    },
    
    startScrolling() {
      this.scrollInterval = setInterval(() => {
        if (this.currentIndex < this.fishDetections.length) {
          this.visibleDetections.shift();
          
          const newItem = { 
            ...this.fishDetections[this.currentIndex], 
            highlight: true 
          };
          this.visibleDetections.push(newItem);
          
          setTimeout(() => {
            if (this.visibleDetections.length > 0) {
              this.visibleDetections[this.visibleDetections.length - 1].highlight = false;
            }
          }, 1000);
          
          this.currentIndex++;
        } else {
          this.currentIndex = 0;
          this.initVisibleData();
        }
      }, 2000);
    }
  }
};
</script>

<style scoped>
.viewfish-container {
  width: 100%;
  height: 100%;
  color: #ddd;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  padding: 10px;
}

.loading, .error {
  padding: 20px;
  text-align: center;
  font-size: 16px;
}

.error {
  color: #ff6b6b;
}

.header {
  display: flex;
  background-color: rgba(13, 36, 81, 0.7);
  padding: 8px 5px;
  font-weight: bold;
  border-bottom: 1px solid #0D2451;
}

.header-item {
  flex: 1;
  text-align: center;
  font-size: 12px;
}

.fish-data-container {
  flex: 1;
  overflow: hidden;
  position: relative;
}

.fish-data-row {
  display: flex;
  padding: 8px 5px;
  border-bottom: 1px solid rgba(13, 36, 81, 0.5);
  transition: background-color 0.3s ease;
}

.fish-data-row.highlight {
  background-color: rgba(0, 255, 255, 0.15);
}

.data-item {
  flex: 1;
  text-align: center;
  font-size: 13px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

/* 不同鱼类种类的颜色 */
.fish-species-1 {
  color: #FF5733;
}

.fish-species-4 {
  color: #33FF57;
}

.fish-species-8 {
  color: #3357FF;
}

.fish-species-0 {
  color: #FFFF33;
}
</style>