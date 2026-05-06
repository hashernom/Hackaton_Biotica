<template>
  <aside class="chat-summary">
    <div class="summary-header">
      <span class="summary-icon">📋</span>
      <span class="summary-title">Datos del Lead</span>
      <span v-if="finalizado" class="badge-done">Calificado ✓</span>
    </div>

    <div class="summary-body">
      <SummaryRow icon="👤" label="Nombre"     :value="lead.nombre" />
      <SummaryRow icon="📞" label="Contacto"   :value="lead.contacto" />
      <SummaryRow icon="🏗️" label="Proyecto"   :value="lead.proyecto" />
      <SummaryRow icon="📍" label="Ubicación"  :value="lead.ubicacion" />
      <SummaryRow
        v-if="lead.clasificacion"
        icon="📁"
        label="Servicio"
        :value="lead.clasificacion"
      />
      <SummaryRow
        v-if="lead.urgencia"
        icon="⚡"
        label="Urgencia"
        :value="lead.urgencia"
        :highlight="lead.urgencia === 'Alta'"
      />
    </div>

    <div class="summary-footer">
      <div class="progress-wrap">
        <div class="progress-label">
          Completitud <strong>{{ completeness }}%</strong>
        </div>
        <div class="progress-bar">
          <div class="progress-fill" :style="{ width: completeness + '%' }" />
        </div>
      </div>

      <button v-if="messageCount > 1" class="reset-btn" @click="$emit('reset')">
        🔄 Nueva consulta
      </button>
    </div>
  </aside>
</template>

<script>
const SummaryRow = {
  name: 'SummaryRow',
  props: { icon: String, label: String, value: String, highlight: Boolean },
  template: `
    <div class="summary-row" :class="{ 'row-highlight': highlight }">
      <span class="row-icon">{{ icon }}</span>
      <div class="row-data">
        <span class="row-label">{{ label }}</span>
        <span class="row-value" :class="value === 'N/A' || value === 'No proporcionado' ? 'row-empty' : ''">
          {{ value || 'N/A' }}
        </span>
      </div>
    </div>
  `
}

export default {
  name: 'ChatSummary',
  components: { SummaryRow },
  props: {
    lead: { type: Object, required: true },
    finalizado: { type: Boolean, default: false },
    messageCount: { type: Number, default: 0 }
  },
  emits: ['reset'],
  computed: {
    completeness() {
      const fields = [
        this.lead.nombre !== 'N/A',
        this.lead.contacto !== 'N/A',
        this.lead.proyecto !== 'N/A',
        this.lead.ubicacion !== 'N/A',
        !!this.lead.clasificacion
      ]
      return Math.round((fields.filter(Boolean).length / fields.length) * 100)
    }
  }
}
</script>

<style scoped>
.chat-summary {
  background: var(--color-white);
  border-left: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 0;
  height: 100%;
  min-width: 240px;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 14px 16px;
  border-bottom: 1px solid var(--color-border);
  background: var(--color-dark);
  color: var(--color-white);
}

.summary-icon { font-size: 1.1rem; }
.summary-title {
  font-family: var(--font-display);
  font-size: 0.95rem;
  font-weight: 700;
  flex: 1;
}

.badge-done {
  font-size: 0.68rem;
  font-weight: 700;
  background: var(--color-primary);
  color: #fff;
  padding: 2px 8px;
  border-radius: 20px;
}

.summary-body {
  flex: 1;
  padding: 12px;
  display: flex;
  flex-direction: column;
  gap: 2px;
  overflow-y: auto;
}

.summary-row {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  padding: 8px 8px;
  border-radius: var(--radius-sm);
  transition: background var(--transition);
}
.summary-row:hover { background: var(--color-bg); }
.row-highlight { background: #fff4e6 !important; }

.row-icon { font-size: 0.9rem; margin-top: 1px; }

.row-data {
  display: flex;
  flex-direction: column;
  gap: 1px;
  min-width: 0;
}

.row-label {
  font-size: 0.65rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--color-muted);
}

.row-value {
  font-size: 0.82rem;
  font-weight: 500;
  color: var(--color-text);
  word-break: break-word;
}

.row-empty { color: var(--color-muted); font-style: italic; }

.summary-footer {
  padding: 12px 16px;
  border-top: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.progress-label {
  font-size: 0.72rem;
  color: var(--color-muted);
  margin-bottom: 4px;
}

.progress-bar {
  height: 6px;
  background: var(--color-border);
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  border-radius: 4px;
  transition: width 0.5s ease;
}

.reset-btn {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-muted);
  padding: 6px 12px;
  border-radius: var(--radius-sm);
  border: 1.5px solid var(--color-border);
  transition: all var(--transition);
  text-align: center;
}

.reset-btn:hover {
  border-color: var(--color-primary);
  color: var(--color-primary-dark);
  background: var(--color-bg);
}
</style>