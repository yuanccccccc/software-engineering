<template>
  <div class="ai-advice-container">
    <!-- 聊天记录区域 - 可滚动 -->
    <div class="chat-history" ref="chatHistory">
      <div v-if="messages.length === 0" class="empty-message">
        请输入问题，AI将为您提供建议...
      </div>
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message-item"
      >
        <!-- 用户消息 -->
        <div class="user-message">
          <div class="message-bubble user-bubble">
            {{ message.question }}
          </div>
        </div>
        <!-- AI回复 -->
        <div class="ai-message">
          <div
            class="message-bubble ai-bubble"
            :class="{ loading: message.isLoading }"
          >
            <span v-if="message.isLoading" class="loading-text"
              >AI正在思考...</span
            >
            <span v-else>{{ message.answer }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 输入区域 - 绝对定位固定在底部 -->
    <div class="input-area">
      <textarea
        v-model="inputText"
        placeholder="请输入您的问题..."
        class="input-textarea"
        @keyup.enter="handleSend"
        :disabled="isLoading"
      ></textarea>
      <button
        @click="handleSend"
        class="send-button"
        :disabled="!inputText.trim() || isLoading"
      >
        <span v-if="isLoading">发送中...</span>
        <span v-else>发送</span>
      </button>
    </div>
  </div>
</template>

<script>
import axios from "axios";

// 根据你的后端配置修改API基础URL
const API_BASE = "http://localhost:5000/api";

export default {
  name: "AI_advice",
  data() {
    return {
      inputText: "",
      messages: [], // 存储聊天记录
      isLoading: false, // 加载状态
    };
  },
  methods: {
    async handleSend() {
      if (this.inputText.trim() && !this.isLoading) {
        const userQuestion = this.inputText.trim();

        // 添加新的对话到记录中（先显示用户问题，AI回答暂时为加载状态）
        const messageIndex = this.messages.length;
        this.messages.push({
          question: userQuestion,
          answer: "",
          isLoading: true,
        });

        // 清空输入框
        this.inputText = "";
        this.isLoading = true;

        // 滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom();
        });

        try {
          // 调用AI API
          const aiResponse = await this.generateAIResponse(userQuestion);

          // 更新消息状态
          this.messages[messageIndex].answer = aiResponse;
          this.messages[messageIndex].isLoading = false;
        } catch (error) {
          // 处理错误
          this.messages[messageIndex].answer =
            "抱歉，AI服务暂时不可用，请稍后再试。";
          this.messages[messageIndex].isLoading = false;
          console.error("AI请求失败:", error);
        } finally {
          this.isLoading = false;

          // 滚动到底部
          this.$nextTick(() => {
            this.scrollToBottom();
          });
        }
      }
    },

    async generateAIResponse(question) {
      try {
        const response = await axios.post(
          `${API_BASE}/ai/chat`,
          {
            question: question,
          },
          {
            timeout: 30000, // 30秒超时
            headers: {
              "Content-Type": "application/json",
            },
          }
        );

        if (response.data.status === "success") {
          return response.data.answer;
        } else {
          throw new Error(response.data.error || "AI服务返回错误");
        }
      } catch (error) {
        if (error.code === "ECONNABORTED") {
          throw new Error("请求超时，请稍后再试");
        } else if (error.response) {
          // 服务器响应了错误状态码
          const errorMsg =
            error.response.data?.error ||
            `服务器错误 (${error.response.status})`;
          throw new Error(errorMsg);
        } else if (error.request) {
          // 请求发出但没有收到响应
          throw new Error("网络连接失败，请检查网络或后端服务是否运行");
        } else {
          // 其他错误
          throw new Error(error.message || "未知错误");
        }
      }
    },

    scrollToBottom() {
      const chatHistory = this.$refs.chatHistory;
      if (chatHistory) {
        chatHistory.scrollTop = chatHistory.scrollHeight;
      }
    },
  },
};
</script>

<style scoped>
.ai-advice-container {
  height: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 20px 10px 10px 10px;
  box-sizing: border-box;
}

.chat-history {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  background: rgba(13, 19, 65, 0.2);
  border: 1px solid #0d2451;
  border-radius: 4px;
  margin-bottom: 5px;
  max-height: 240px;
  min-height: 20px;
}

.empty-message {
  color: #8cbccd;
  text-align: center;
  font-size: 12px;
  margin-top: 50px;
  opacity: 0.7;
}

.message-item {
  margin-bottom: 15px;
}

.user-message {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 8px;
}

.ai-message {
  display: flex;
  justify-content: flex-start;
}

.message-bubble {
  max-width: 80%;
  padding: 8px 12px;
  border-radius: 12px;
  font-size: 12px;
  line-height: 1.4;
  word-wrap: break-word;
}

.user-bubble {
  background: #36cbcb;
  color: #fff;
  border-bottom-right-radius: 4px;
}

.ai-bubble {
  background: rgba(13, 19, 65, 0.8);
  color: #fff;
  border: 1px solid #0d2451;
  border-bottom-left-radius: 4px;
}

.ai-bubble.loading {
  opacity: 0.7;
}

.loading-text {
  font-style: italic;
  opacity: 0.8;
  animation: pulse 1.5s infinite;
}

@keyframes pulse {
  0%,
  100% {
    opacity: 0.8;
  }
  50% {
    opacity: 0.4;
  }
}

.input-area {
  flex-shrink: 0;
  height: 40px;
  display: flex;
  gap: 8px;
  align-items: center;
  background: #151456;
  padding: 5px;
  border-radius: 4px;
  border: 1px solid #0d2451;
  box-sizing: border-box;
}

.input-textarea {
  flex: 1;
  height: 30px;
  padding: 6px 8px;
  border: 1px solid #0d2451;
  background: #0d1341;
  color: #fff;
  font-size: 12px;
  resize: none;
  border-radius: 4px;
  outline: none;
}

.input-textarea:focus {
  border-color: #36cbcb;
}

.input-textarea:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-textarea::placeholder {
  color: #8cbccd;
}

.send-button {
  padding: 6px 12px;
  background: #36cbcb;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 12px;
  transition: background 0.3s;
  height: 30px;
  flex-shrink: 0;
  min-width: 60px;
}

.send-button:hover:not(:disabled) {
  background: #2ba8a8;
}

.send-button:disabled {
  background: #666;
  cursor: not-allowed;
}

/* 滚动条样式 */
.chat-history::-webkit-scrollbar {
  width: 4px;
}

.chat-history::-webkit-scrollbar-track {
  background: rgba(13, 36, 81, 0.3);
}

.chat-history::-webkit-scrollbar-thumb {
  background: #36cbcb;
  border-radius: 2px;
}
</style>
