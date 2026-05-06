<template>
  <div class="chat-box" ref="boxRef">
    <ChatMessage
      v-for="(msg, i) in messages"
      :key="i"
      :message="msg"
    />
    <TypingLoader v-if="isLoading" />
    <div ref="bottomAnchor" />
  </div>
</template>

<script>
import ChatMessage from './ChatMessage.vue'
import TypingLoader from './TypingLoader.vue'
import { scrollToBottom } from '@/utils/helpers'

export default {
  name: 'ChatBox',
  components: { ChatMessage, TypingLoader },
  props: {
    messages: { type: Array, default: () => [] },
    isLoading: { type: Boolean, default: false }
  },
  watch: {
    messages() {
      this.$nextTick(() => scrollToBottom(this.$refs.boxRef))
    },
    isLoading(val) {
      if (val) this.$nextTick(() => scrollToBottom(this.$refs.boxRef))
    }
  },
  mounted() {
    scrollToBottom(this.$refs.boxRef)
  }
}
</script>

<style scoped>
.chat-box {
  flex: 1;
  overflow-y: auto;
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  background: var(--chat-area-bg);
  background-image:
    radial-gradient(circle at 20% 80%, rgba(84,180,53,0.05) 0%, transparent 50%),
    radial-gradient(circle at 80% 20%, rgba(160,191,27,0.04) 0%, transparent 50%);
}
</style>