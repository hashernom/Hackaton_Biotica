/**
 * Format a timestamp into a readable time string (HH:MM).
 * @param {number} ts - Unix timestamp in ms
 * @returns {string}
 */
export function formatTime(ts) {
  const d = new Date(ts)
  return d.toLocaleTimeString('es-CO', { hour: '2-digit', minute: '2-digit' })
}

/**
 * Parse Markdown-like bold (**text**) and line breaks into HTML.
 * Lightweight, no dependency needed.
 * @param {string} text
 * @returns {string}
 */
export function parseMarkdown(text) {
  if (!text) return ''
  return text
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.*?)\*/g, '<em>$1</em>')
    .replace(/\n/g, '<br>')
}

/**
 * Generate a short random session ID.
 * @returns {string}
 */
export function generateSessionId() {
  return Math.random().toString(36).substring(2, 10).toUpperCase()
}

/**
 * Scroll an element to its bottom (for chat containers).
 * @param {HTMLElement} el
 */
export function scrollToBottom(el) {
  if (!el) return
  el.scrollTop = el.scrollHeight
}

/**
 * Debounce utility.
 */
export function debounce(fn, ms = 300) {
  let timer
  return (...args) => {
    clearTimeout(timer)
    timer = setTimeout(() => fn(...args), ms)
  }
}