<template>
  <div class="message">{{ message }}</div>
</template>

<script>
export default {
  name: 'AI_advice',
  data() {
    return {
      message: '待接入API'
    }
  }
}
</script>

<style scoped>
.message {
  font-size: 13px;
  color: #333;
  padding: 16px;

}
</style>
