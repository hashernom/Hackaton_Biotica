<template>
  <div class="chat-input-wrapper">
    <!-- Quick replies (shown only at start) -->
    <div v-if="showQuickReplies" class="quick-replies">
      <button
        v-for="qr in quickReplies"
        :key="qr"
        class="qr-chip"
        @click="sendQuick(qr)"
        :disabled="disabled"
      >{{ qr }}</button>
    </div>

    <!-- Input bar -->
    <form class="input-bar" @submit.prevent="send">
      <textarea
        ref="inputRef"
        v-model="text"
        class="input-field"
        placeholder="Escribe tu mensaje..."
        rows="1"
        :disabled="disabled"
        @keydown.enter.exact.prevent="send"
        @input="autoResize"
      />
      <button
        type="submit"
        class="send-btn"
        :disabled="disabled || !text.trim()"
        :class="{ active: text.trim() }"
      >
        <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
        </svg>
      </button>
    </form>
  </div>
</template>

<script>
import { QUICK_REPLIES } from '@/utils/constants'

export default {
  name: 'ChatInput',
  props: {
    disabled: { type: Boolean, default: false },
    showQuickReplies: { type: Boolean, default: true }
  },
  emits: ['send'],
  data() {
    return {
      text: '',
      quickReplies: QUICK_REPLIES
    }
  },
  methods: {
    send() {
      const msg = this.text.trim()
      if (!msg || this.disabled) return
      this.$emit('send', msg)
      this.text = ''
      this.$nextTick(() => {
        if (this.$refs.inputRef) {
          this.$refs.inputRef.style.height = 'auto'
        }
      })
    },
    sendQuick(qr) {
      this.$emit('send', qr)
    },
    autoResize() {
      const el = this.$refs.inputRef
      if (!el) return
      el.style.height = 'auto'
      el.style.height = Math.min(el.scrollHeight, 120) + 'px'
    }
  }
}
</script>

<style scoped>
.chat-input-wrapper {
  border-top: 1px solid var(--color-border);
  background: var(--color-white);
  padding: 12px 16px 16px;
}

.quick-replies {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 10px;
}

.qr-chip {
  font-size: 0.78rem;
  font-weight: 500;
  padding: 5px 12px;
  border-radius: 20px;
  border: 1.5px solid var(--color-border);
  color: var(--color-dark);
  background: var(--color-bg);
  transition: all var(--transition);
  cursor: pointer;
  white-space: nowrap;
}

.qr-chip:hover:not(:disabled) {
  border-color: var(--color-primary);
  background: #e8f8df;
  color: var(--color-primary-dark);
}

.qr-chip:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.input-bar {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  background: var(--color-bg);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: 6px 6px 6px 16px;
  transition: border-color var(--transition), box-shadow var(--transition);
}

.input-bar:focus-within {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(84,180,53,0.12);
}

.input-field {
  flex: 1;
  border: none;
  background: transparent;
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--color-text);
  resize: none;
  line-height: 1.5;
  max-height: 120px;
  outline: none;
  padding: 5px 0;
}

.input-field::placeholder { color: var(--color-muted); }

.send-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--color-border);
  color: var(--color-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: all var(--transition);
}

.send-btn.active {
  background: var(--color-primary);
  color: var(--color-white);
  box-shadow: 0 2px 10px rgba(84,180,53,0.35);
}

.send-btn.active:hover {
  background: var(--color-primary-light);
  transform: scale(1.06);
}

.send-btn:disabled {
  cursor: not-allowed;
  transform: none !important;
}
</style>