<template>
  <div class="chat-view">
    <!-- Header bar -->
    <div class="chat-topbar">
      <div class="topbar-info">
        <div class="bot-avatar">🌿</div>
        <div class="bot-details">
          <span class="bot-name">AsistenteBiótica</span>
          <span class="bot-status">
            <span class="status-dot" :class="{ pulse: isLoading }" />
            {{ isLoading ? 'Analizando...' : 'En línea' }}
          </span>
        </div>
      </div>
      <div class="topbar-actions">
        <span v-if="isUrgente" class="urgencia-badge">🔥 Caso Urgente</span>
        <span v-if="isLeadFinalizado" class="done-badge">✅ Lead Calificado</span>
        <button class="icon-btn" title="Nueva consulta" @click="resetChat">
          <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 .49-3.5"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Chat area + summary panel -->
    <div class="chat-layout">
      <div class="chat-main">
        <ChatBox :messages="messages" :is-loading="isLoading" />
        <ChatInput
          :disabled="isLoading"
          :show-quick-replies="messages.length <= 1"
          @send="onSend"
        />
      </div>

      <!-- Side panel (desktop only) -->
      <ChatSummary
        class="chat-sidebar"
        :lead="leadData"
        :finalizado="isLeadFinalizado"
        :message-count="messages.length"
        @reset="resetChat"
      />
    </div>

    <!-- Toast notification -->
    <transition name="toast">
      <div v-if="toast.visible" class="toast-notification" :class="toast.type">
        {{ toast.message }}
      </div>
    </transition>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import ChatBox from '@/components/chat/ChatBox.vue'
import ChatInput from '@/components/chat/ChatInput.vue'
import ChatSummary from '@/components/chat/ChatSummary.vue'
import { WELCOME_MESSAGE } from '@/utils/constants'

export default {
  name: 'ChatView',
  components: { ChatBox, ChatInput, ChatSummary },

  data() {
    return {
      toast: { visible: false, message: '', type: 'success', timer: null }
    }
  },

  computed: {
    ...mapGetters(['messages', 'isLoading', 'leadData', 'isLeadFinalizado', 'isUrgente'])
  },

  watch: {
    isLeadFinalizado(val) {
      if (val) this.showToast('🚀 Lead calificado y enviado al sistema central', 'success')
    },
    isUrgente(val) {
      if (val) this.showToast('🔥 Caso urgente detectado — prioridad alta', 'urgent')
    }
  },

  mounted() {
    if (this.messages.length === 0) {
      this.$store.commit('ADD_MESSAGE', { ...WELCOME_MESSAGE })
    }
  },

  methods: {
    ...mapActions(['sendMessage', 'resetChat']),

    async onSend(text) {
      await this.sendMessage(text)
    },

    showToast(message, type = 'success') {
      clearTimeout(this.toast.timer)
      this.toast = { visible: true, message, type, timer: null }
      this.toast.timer = setTimeout(() => { this.toast.visible = false }, 4000)
    },

    resetChat() {
      this.$store.dispatch('resetChat')
      this.$nextTick(() => {
        this.$store.commit('ADD_MESSAGE', { ...WELCOME_MESSAGE, ts: Date.now() })
      })
    }
  }
}
</script>

<style scoped>
.chat-view {
  flex: 1;
  display: flex;
  flex-direction: column;
  height: calc(100vh - 64px);
  position: relative;
  overflow: hidden;
}

/* Top bar */
.chat-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 20px;
  background: var(--color-white);
  border-bottom: 1px solid var(--color-border);
  box-shadow: var(--shadow-sm);
  z-index: 10;
}

.topbar-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.bot-avatar {
  width: 42px;
  height: 42px;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  box-shadow: 0 2px 10px rgba(84,180,53,0.3);
}

.bot-details {
  display: flex;
  flex-direction: column;
}

.bot-name {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
}

.bot-status {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 0.75rem;
  color: var(--color-muted);
}

.status-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
}

.status-dot.pulse {
  animation: pulse 1s infinite;
  background: var(--color-secondary);
}

.topbar-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.urgencia-badge {
  font-size: 0.72rem;
  font-weight: 700;
  background: #fff3e0;
  color: #e65100;
  border: 1px solid #ffcc80;
  padding: 3px 10px;
  border-radius: 20px;
}

.done-badge {
  font-size: 0.72rem;
  font-weight: 700;
  background: #e8f5e9;
  color: var(--color-primary-dark);
  border: 1px solid var(--color-primary);
  padding: 3px 10px;
  border-radius: 20px;
}

.icon-btn {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1.5px solid var(--color-border);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-muted);
  transition: all var(--transition);
}

.icon-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: var(--color-bg);
}

/* Layout */
.chat-layout {
  flex: 1;
  display: flex;
  overflow: hidden;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-sidebar {
  width: 260px;
  flex-shrink: 0;
  overflow-y: auto;
}

/* Toast */
.toast-notification {
  position: absolute;
  bottom: 90px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-dark);
  color: white;
  font-size: 0.83rem;
  font-weight: 600;
  padding: 10px 20px;
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow-lg);
  white-space: nowrap;
  z-index: 50;
}

.toast-notification.success { background: var(--color-dark); border-left: 4px solid var(--color-primary); }
.toast-notification.urgent  { background: #3d1a00; border-left: 4px solid #ff6d00; }

.toast-enter-active, .toast-leave-active { transition: all 0.35s ease; }
.toast-enter-from, .toast-leave-to { opacity: 0; transform: translateX(-50%) translateY(16px); }

/* Responsive: hide sidebar on mobile */
@media (max-width: 768px) {
  .chat-sidebar { display: none; }
}
</style>