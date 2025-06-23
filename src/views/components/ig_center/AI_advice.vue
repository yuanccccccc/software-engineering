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
          <div class="message-bubble ai-bubble">
            {{ message.answer }}
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
      ></textarea>
      <button
        @click="handleSend"
        class="send-button"
        :disabled="!inputText.trim()"
      >
        发送
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: "AI_advice",
  data() {
    return {
      inputText: "",
      messages: [], // 存储聊天记录
    };
  },
  methods: {
    handleSend() {
      if (this.inputText.trim()) {
        // 添加新的对话到记录中
        this.messages.push({
          question: this.inputText.trim(),
          answer: this.generateAIResponse(this.inputText.trim()),
        });

        // 清空输入框
        this.inputText = "";

        // 滚动到底部
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      }
    },

    generateAIResponse(question) {
      // 模拟AI响应
      const responses = [
        "根据您的问题，建议加强海洋环境监测。",
        "建议优化鱼类养殖密度，确保水质稳定。",
        "可以考虑调整投喂策略，提高鱼类生长效率。",
        "建议关注水温变化，及时调节养殖环境。",
        "推荐增加水质检测频率，预防疾病发生。",
      ];
      return responses[Math.floor(Math.random() * responses.length)];
    },

    scrollToBottom() {
      const chatHistory = this.$refs.chatHistory;
      chatHistory.scrollTop = chatHistory.scrollHeight;
    },
  },
};
</script>

<style scoped>
.ai-advice-container {
  height: 100%;
  position: relative; /* 重要：为绝对定位的子元素提供参考 */
  display: flex;
  flex-direction: column;
  padding: 20px 10px 10px 10px;
  box-sizing: border-box;
}

.chat-history {
  flex: 1; /* 占满剩余空间 */
  overflow-y: auto;
  padding: 10px;
  background: rgba(13, 19, 65, 0.2);
  border: 1px solid #0d2451;
  border-radius: 4px;
  margin-bottom: 5px; /* 与输入框的间距 */
  max-height: 240px; /* 添加最大高度限制 */
  min-height: 20px; /* 添加最小高度 */
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

.input-area {
  flex-shrink: 0; /* 防止输入框被压缩 */
  height: 40px; /* 固定高度 */
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
  flex-shrink: 0; /* 防止按钮被压缩 */
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
