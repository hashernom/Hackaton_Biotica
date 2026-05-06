<template>
  <div class="msg-row assistant">
    <div class="msg-avatar">🌿</div>
    <div class="typing-bubble">
      <span class="dot" />
      <span class="dot" />
      <span class="dot" />
    </div>
  </div>
</template>

<script>
export default { name: 'TypingLoader' }
</script>

<style scoped>
.msg-row {
  display: flex;
  align-items: flex-end;
  gap: 10px;
  margin-bottom: 1rem;
  animation: fadeUp 0.25s ease both;
}

.msg-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  flex-shrink: 0;
  box-shadow: var(--shadow-sm);
}

.typing-bubble {
  display: flex;
  align-items: center;
  gap: 5px;
  background: var(--color-white);
  padding: 14px 18px;
  border-radius: var(--radius-md);
  border-bottom-left-radius: 4px;
  box-shadow: var(--shadow-sm);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--color-primary);
  display: inline-block;
  animation: pulse 1.2s infinite ease-in-out;
}

.dot:nth-child(2) { animation-delay: 0.2s; background: var(--color-secondary); }
.dot:nth-child(3) { animation-delay: 0.4s; background: var(--color-dark); }
</style>