<template>
  <div class="msg-row" :class="message.role">
    <!-- Avatar -->
    <div class="msg-avatar">
      <span v-if="message.role === 'assistant'">🌿</span>
      <span v-else>👤</span>
    </div>

    <!-- Bubble -->
    <div class="msg-bubble" :class="{ 'bubble-error': message.error }">
      <div class="bubble-content" v-html="parsedContent" />

      <!-- Lead badge for assistant messages -->
      <div v-if="message.meta && message.meta.clasificacion && message.meta.clasificacion !== 'Error'" class="bubble-meta">
        <span class="meta-tag">
          📁 {{ message.meta.clasificacion }}
        </span>
        <span class="meta-tag" :class="message.meta.urgencia === 'Alta' ? 'meta-urgent' : ''">
          {{ message.meta.urgencia === 'Alta' ? '🔥 Urgente' : '✅ Normal' }}
        </span>
        <span v-if="message.meta.finalizado" class="meta-tag meta-done">
          🚀 Lead calificado
        </span>
      </div>

      <span class="bubble-time">{{ time }}</span>
    </div>
  </div>
</template>

<script>
import { parseMarkdown, formatTime } from '@/utils/helpers'

export default {
  name: 'ChatMessage',
  props: {
    message: {
      type: Object,
      required: true
    }
  },
  computed: {
    parsedContent() {
      return parseMarkdown(this.message.content)
    },
    time() {
      return this.message.ts ? formatTime(this.message.ts) : ''
    }
  }
}
</script>

<style scoped>
.msg-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin-bottom: 1rem;
  animation: fadeUp 0.3s ease both;
}

.msg-row.user {
  flex-direction: row-reverse;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.assistant .msg-avatar {
  background: var(--color-primary);
}

.user .msg-avatar {
  background: var(--color-dark);
}

.msg-bubble {
  max-width: 72%;
  padding: 12px 16px 8px;
  border-radius: var(--radius-md);
  position: relative;
  box-shadow: var(--shadow-sm);
}

.assistant .msg-bubble {
  background: var(--chat-bot-bg);
  color: var(--chat-bot-text);
  border-bottom-left-radius: 4px;
}

.user .msg-bubble {
  background: var(--chat-user-bg);
  color: var(--chat-user-text);
  border-bottom-right-radius: 4px;
}

.bubble-error {
  background: #fff3f3 !important;
  border: 1px solid #f5c2c2;
}

.bubble-content {
  font-size: 0.92rem;
  line-height: 1.6;
}

.bubble-time {
  display: block;
  font-size: 0.7rem;
  opacity: 0.45;
  margin-top: 5px;
  text-align: right;
}

.bubble-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid var(--color-border);
}

.meta-tag {
  font-size: 0.68rem;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 20px;
  background: var(--color-bg);
  color: var(--color-muted);
  border: 1px solid var(--color-border);
}

.meta-urgent {
  background: #fff4e6;
  color: #c46800;
  border-color: #ffd59a;
}

.meta-done {
  background: #e8f8df;
  color: var(--color-primary-dark);
  border-color: var(--color-primary);
}
</style>