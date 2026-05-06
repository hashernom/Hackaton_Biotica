<template>
  <div class="admin-view">
    <!-- Topbar admin -->
    <div class="admin-topbar">
      <div class="topbar-left">
        <span class="topbar-icon">📊</span>
        <div>
          <h1 class="topbar-title">Panel de Control</h1>
          <span class="topbar-sub">Bienvenido, <strong>{{ adminUsuario }}</strong></span>
        </div>
      </div>
      <div class="topbar-actions">
        <button class="btn-refresh" @click="cargarTodo" :disabled="adminLoading">
          {{ adminLoading ? '⏳ Cargando...' : '🔄 Actualizar' }}
        </button>
        <button class="btn-export excel" @click="exportarExcel">📥 Excel</button>
        <button class="btn-export csv"   @click="exportarCSV">📄 CSV</button>
        <button class="btn-logout" @click="cerrarSesion">Cerrar sesión →</button>
      </div>
    </div>

    <div class="admin-body container">

      <!-- ── Métricas rápidas ───────────────────────────────────────── -->
      <div class="metricas-grid" v-if="adminMetricas">
        <div class="metrica-card" v-for="m in tarjetasMetricas" :key="m.label" :class="m.class">
          <span class="m-icon">{{ m.icon }}</span>
          <div>
            <p class="m-valor">{{ m.valor }}</p>
            <p class="m-label">{{ m.label }}</p>
          </div>
        </div>
      </div>

      <!-- ── Tabs ───────────────────────────────────────────────────── -->
      <div class="tabs">
        <button
          v-for="tab in tabs"
          :key="tab.id"
          class="tab-btn"
          :class="{ active: tabActivo === tab.id }"
          @click="tabActivo = tab.id"
        >{{ tab.label }}</button>
      </div>

      <!-- ── Tab: Indicadores de desempeño ─────────────────────────── -->
      <div v-if="tabActivo === 'indicadores'" class="tab-content">
        <div v-if="adminStats" class="charts-grid">

          <!-- KPIs de desempeño -->
          <div class="kpi-row">
            <div class="kpi-card">
              <p class="kpi-num green">{{ adminStats.pct_filtradas }}%</p>
              <p class="kpi-label">Solicitudes filtradas<br>(Fuera de alcance)</p>
            </div>
            <div class="kpi-card">
              <p class="kpi-num orange">{{ adminStats.pct_urgentes }}%</p>
              <p class="kpi-label">Solicitudes urgentes</p>
            </div>
            <div class="kpi-card">
              <p class="kpi-num blue">{{ adminStats.total_leads }}</p>
              <p class="kpi-label">Total leads procesados</p>
            </div>
          </div>

          <!-- Gráfico barras: por clasificación -->
          <div class="chart-card">
            <h3 class="chart-title">📁 Solicitudes por Servicio</h3>
            <div class="bar-chart">
              <div
                v-for="item in adminStats.por_clasificacion"
                :key="item.servicio"
                class="bar-row"
              >
                <span class="bar-name">{{ item.servicio }}</span>
                <div class="bar-track">
                  <div
                    class="bar-fill"
                    :style="{ width: barPct(item.total, maxClasificacion) + '%' }"
                  />
                </div>
                <span class="bar-count">{{ item.total }}</span>
              </div>
            </div>
          </div>

          <!-- Gráfico dona: urgencia -->
          <div class="chart-card chart-small">
            <h3 class="chart-title">⚡ Por Urgencia</h3>
            <div class="dona-wrap">
              <svg viewBox="0 0 100 100" class="dona-svg">
                <circle cx="50" cy="50" r="40" fill="none" stroke="var(--color-border)" stroke-width="16"/>
                <circle
                  cx="50" cy="50" r="40" fill="none"
                  stroke="var(--color-primary)" stroke-width="16"
                  stroke-dasharray="251.2"
                  :stroke-dashoffset="donaOffset"
                  transform="rotate(-90 50 50)"
                  stroke-linecap="round"
                />
              </svg>
              <div class="dona-center">
                <p class="dona-pct">{{ adminStats.pct_urgentes }}%</p>
                <p class="dona-sub">Urgentes</p>
              </div>
            </div>
            <div class="dona-leyenda">
              <span v-for="u in adminStats.por_urgencia" :key="u.nivel" class="leyenda-item">
                <span class="leyenda-dot" :class="u.nivel === 'Alta' ? 'dot-urgent' : 'dot-normal'"/>
                {{ u.nivel }}: <strong>{{ u.total }}</strong>
              </span>
            </div>
          </div>

          <!-- Gráfico línea: por día -->
          <div class="chart-card chart-wide">
            <h3 class="chart-title">📈 Solicitudes por Día (últimos 30 días)</h3>
            <div class="line-chart-wrap">
              <svg :viewBox="`0 0 ${lineW} ${lineH}`" class="line-svg" v-if="linePoints.length > 1">
                <!-- Grid lines -->
                <line v-for="i in 4" :key="i"
                  :x1="pad" :x2="lineW - pad"
                  :y1="lineH - pad - ((i-1) * (lineH - 2*pad) / 3)"
                  :y2="lineH - pad - ((i-1) * (lineH - 2*pad) / 3)"
                  stroke="var(--color-border)" stroke-width="1"
                />
                <!-- Área de relleno -->
                <path :d="areaPath" fill="rgba(84,180,53,0.1)" />
                <!-- Línea -->
                <polyline :points="linePoints" fill="none" stroke="var(--color-primary)" stroke-width="2.5" stroke-linejoin="round"/>
                <!-- Puntos -->
                <circle v-for="(p, i) in lineDotsData" :key="i"
                  :cx="p.x" :cy="p.y" r="3.5"
                  fill="var(--color-primary)" stroke="white" stroke-width="1.5"
                />
              </svg>
              <p v-else class="chart-empty">No hay datos de los últimos 30 días.</p>
            </div>
          </div>

        </div>
        <div v-else class="empty-state">
          <p>⏳ Cargando indicadores...</p>
        </div>
      </div>

      <!-- ── Tab: Leads / Solicitudes ───────────────────────────────── -->
      <div v-if="tabActivo === 'leads'" class="tab-content">
        <div class="leads-toolbar">
          <input v-model="busqueda" class="search-input" placeholder="🔍 Buscar por nombre, servicio..."/>
          <select v-model="filtroUrgencia" class="filter-select">
            <option value="">Todas las urgencias</option>
            <option value="Alta">🔥 Alta</option>
            <option value="Normal">✅ Normal</option>
          </select>
        </div>

        <div class="leads-table-wrap" v-if="leadsFiltrados.length">
          <table class="leads-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Fecha</th>
                <th>Nombre</th>
                <th>Contacto</th>
                <th>Servicio</th>
                <th>Urgencia</th>
                <th>Proyecto</th>
                <th>Ubicación</th>
                <th>Estado</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="l in leadsFiltrados" :key="l.id">
                <td>{{ l.id }}</td>
                <td class="td-fecha">{{ formatFecha(l.fecha) }}</td>
                <td class="td-bold">{{ l.nombre }}</td>
                <td>{{ l.contacto }}</td>
                <td>
                  <span class="badge-servicio">{{ l.clasificacion }}</span>
                </td>
                <td>
                  <span class="badge-urgencia" :class="l.urgencia === 'Alta' ? 'urgent' : 'normal'">
                    {{ l.urgencia === 'Alta' ? '🔥 Alta' : '✅ Normal' }}
                  </span>
                </td>
                <td>{{ l.proyecto }}</td>
                <td>{{ l.ubicacion }}</td>
                <td>
                  <span class="badge-estado">{{ l.siguiente_paso }}</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else class="empty-state">
          <p>📭 No hay leads que coincidan con los filtros.</p>
        </div>
      </div>

      <!-- ── Tab: Historial de Chats ────────────────────────────────── -->
      <div v-if="tabActivo === 'historial'" class="tab-content">
        <div class="historial-layout">
          <!-- Lista de sesiones -->
          <div class="sesiones-list">
            <h3 class="section-label">Sesiones de chat</h3>
            <div
              v-for="s in adminSesiones"
              :key="s.session_id"
              class="sesion-item"
              :class="{ active: sesionActiva === s.session_id }"
              @click="verHistorial(s.session_id)"
            >
              <div class="sesion-id">🗨️ {{ s.session_id }}</div>
              <div class="sesion-meta">
                {{ formatFecha(s.creada_en) }} · {{ s.total_mensajes }} mensajes
              </div>
            </div>
            <p v-if="!adminSesiones.length" class="empty-state small">Sin sesiones registradas.</p>
          </div>

          <!-- Detalle del historial -->
          <div class="historial-detalle">
            <template v-if="adminHistorial">
              <h3 class="section-label">Sesión: {{ adminHistorial.session_id }}</h3>
              <div class="historial-msgs">
                <div
                  v-for="(m, i) in adminHistorial.mensajes"
                  :key="i"
                  class="hm-row"
                  :class="m.role"
                >
                  <span class="hm-avatar">{{ m.role === 'user' ? '👤' : '🌿' }}</span>
                  <div class="hm-bubble">
                    <p class="hm-content">{{ m.content }}</p>
                    <span class="hm-time">{{ m.timestamp }}</span>
                  </div>
                </div>
              </div>
            </template>
            <div v-else class="empty-state">
              <p>👈 Selecciona una sesión para ver el historial.</p>
            </div>
          </div>
        </div>
      </div>

    </div><!-- /admin-body -->
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'
import adminService from '@/services/admin.service'

export default {
  name: 'AdminView',
  data() {
    return {
      tabActivo: 'indicadores',
      tabs: [
        { id: 'indicadores', label: '📈 Indicadores' },
        { id: 'leads',       label: '📋 Leads' },
        { id: 'historial',   label: '🗨️ Historial de Chats' },
      ],
      busqueda:       '',
      filtroUrgencia: '',
      sesionActiva:   null,
      // SVG línea
      lineW: 600, lineH: 160, pad: 30,
    }
  },

  computed: {
    ...mapGetters([
      'adminToken', 'adminUsuario', 'adminLeads', 'adminMetricas',
      'adminStats', 'adminSesiones', 'adminHistorial', 'adminLoading',
    ]),

    tarjetasMetricas() {
      const m = this.adminMetricas
      if (!m) return []
      return [
        { label: 'Leads totales',          valor: m.total_leads,           icon: '📊', class: '' },
        { label: 'Urgencia alta',          valor: m.urgencia_alta,          icon: '🔥', class: 'card-urgent' },
        { label: 'Listos para consultor',  valor: m.listos_para_consultor,  icon: '✅', class: 'card-ok' },
        { label: 'Fuera de alcance',       valor: m.fuera_de_alcance,       icon: '⛔', class: 'card-warn' },
        { label: 'Seguimiento urgente',    valor: m.seguimiento_urgente,    icon: '⚡', class: 'card-urgent' },
      ]
    },

    leadsFiltrados() {
      let lista = this.adminLeads || []
      if (this.filtroUrgencia) lista = lista.filter(l => l.urgencia === this.filtroUrgencia)
      if (this.busqueda) {
        const q = this.busqueda.toLowerCase()
        lista = lista.filter(l =>
          (l.nombre || '').toLowerCase().includes(q) ||
          (l.clasificacion || '').toLowerCase().includes(q) ||
          (l.contacto || '').toLowerCase().includes(q) ||
          (l.proyecto || '').toLowerCase().includes(q)
        )
      }
      return lista
    },

    maxClasificacion() {
      if (!this.adminStats?.por_clasificacion?.length) return 1
      return Math.max(...this.adminStats.por_clasificacion.map(i => i.total))
    },

    donaOffset() {
      const pct = this.adminStats?.pct_urgentes || 0
      return 251.2 - (251.2 * pct / 100)
    },

    // SVG línea por día
    lineDotsData() {
      const datos = this.adminStats?.por_dia || []
      if (datos.length < 2) return []
      const maxV = Math.max(...datos.map(d => d.total), 1)
      const W = this.lineW - 2 * this.pad
      const H = this.lineH - 2 * this.pad
      return datos.map((d, i) => ({
        x: this.pad + (i / (datos.length - 1)) * W,
        y: this.lineH - this.pad - (d.total / maxV) * H,
      }))
    },

    linePoints() {
      return this.lineDotsData.map(p => `${p.x},${p.y}`).join(' ')
    },

    areaPath() {
      if (!this.lineDotsData.length) return ''
      const first = this.lineDotsData[0]
      const last  = this.lineDotsData[this.lineDotsData.length - 1]
      const pts   = this.lineDotsData.map(p => `${p.x},${p.y}`).join(' ')
      return `M${first.x},${this.lineH - this.pad} L${pts.split(' ').map(p => p).join(' L')} L${last.x},${this.lineH - this.pad} Z`
    },
  },

  methods: {
    ...mapActions(['adminLogout', 'fetchLeads', 'fetchStats', 'fetchSesiones', 'fetchHistorial']),

    async cargarTodo() {
      await Promise.all([this.fetchLeads(), this.fetchStats(), this.fetchSesiones()])
    },

    async cerrarSesion() {
      await this.adminLogout()
      this.$router.push({ name: 'login' })
    },

    async exportarExcel() {
      await adminService.exportarExcel(this.adminToken)
    },

    async exportarCSV() {
      await adminService.exportarCSV(this.adminToken)
    },

    async verHistorial(sessionId) {
      this.sesionActiva = sessionId
      await this.fetchHistorial(sessionId)
    },

    barPct(val, max) {
      return max > 0 ? Math.max((val / max) * 100, 4) : 4
    },

    formatFecha(f) {
      if (!f) return '—'
      return new Date(f).toLocaleString('es-CO', {
        day: '2-digit', month: '2-digit', year: '2-digit',
        hour: '2-digit', minute: '2-digit'
      })
    },
  },

  mounted() {
    this.cargarTodo()
  },
}
</script>

<style scoped>
/* ── Layout base ─────────────────────────────────────────────── */
.admin-view {
  min-height: calc(100vh - 64px);
  background: var(--color-bg);
  display: flex;
  flex-direction: column;
}

.admin-topbar {
  background: var(--color-dark);
  padding: 14px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 12px;
}

.topbar-left { display: flex; align-items: center; gap: 14px; }
.topbar-icon { font-size: 2rem; }

.topbar-title {
  font-family: var(--font-display);
  font-size: 1.2rem;
  font-weight: 700;
  color: white;
  margin: 0;
}

.topbar-sub {
  font-size: 0.78rem;
  color: rgba(255,255,255,0.55);
}

.topbar-actions { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }

.btn-refresh {
  font-size: 0.82rem;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  border: 1.5px solid rgba(255,255,255,0.2);
  color: white;
  background: transparent;
  cursor: pointer;
  transition: all var(--transition);
}
.btn-refresh:hover:not(:disabled) { background: rgba(255,255,255,0.1); }

.btn-export {
  font-size: 0.82rem;
  font-weight: 700;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  transition: all var(--transition);
}
.btn-export.excel { background: #1d6f42; color: white; }
.btn-export.excel:hover { background: #16543a; }
.btn-export.csv   { background: #0066cc; color: white; }
.btn-export.csv:hover   { background: #0052a3; }

.btn-logout {
  font-size: 0.82rem;
  font-weight: 600;
  padding: 7px 14px;
  border-radius: var(--radius-sm);
  background: rgba(255,255,255,0.08);
  border: 1.5px solid rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.75);
  cursor: pointer;
  transition: all var(--transition);
}
.btn-logout:hover { background: rgba(220,50,50,0.25); color: white; border-color: rgba(220,50,50,0.5); }

.admin-body { padding: 24px 0 40px; }

/* ── Métricas ────────────────────────────────────────────────── */
.metricas-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(170px, 1fr));
  gap: 14px;
  margin-bottom: 28px;
}

.metrica-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 18px 16px;
  display: flex;
  align-items: center;
  gap: 14px;
  box-shadow: var(--shadow-sm);
  border-left: 4px solid var(--color-border);
}

.metrica-card.card-urgent { border-left-color: #e65100; }
.metrica-card.card-ok     { border-left-color: var(--color-primary); }
.metrica-card.card-warn   { border-left-color: var(--color-secondary); }

.m-icon  { font-size: 1.8rem; }
.m-valor {
  font-family: var(--font-display);
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
  line-height: 1;
}
.m-label { font-size: 0.72rem; color: var(--color-muted); margin: 3px 0 0; }

/* ── Tabs ─────────────────────────────────────────────────────── */
.tabs {
  display: flex;
  gap: 4px;
  border-bottom: 2px solid var(--color-border);
  margin-bottom: 24px;
}

.tab-btn {
  font-size: 0.88rem;
  font-weight: 600;
  padding: 10px 20px;
  border: none;
  background: none;
  cursor: pointer;
  color: var(--color-muted);
  border-bottom: 3px solid transparent;
  margin-bottom: -2px;
  transition: all var(--transition);
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.tab-btn:hover  { color: var(--color-text); background: rgba(84,180,53,0.05); }
.tab-btn.active { color: var(--color-primary); border-bottom-color: var(--color-primary); background: rgba(84,180,53,0.06); }

/* ── Charts ───────────────────────────────────────────────────── */
.charts-grid {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.kpi-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.kpi-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 20px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.kpi-num {
  font-family: var(--font-display);
  font-size: 2.2rem;
  font-weight: 700;
  margin: 0 0 4px;
}
.kpi-num.green  { color: var(--color-primary); }
.kpi-num.orange { color: #e65100; }
.kpi-num.blue   { color: #0066cc; }
.kpi-label { font-size: 0.8rem; color: var(--color-muted); line-height: 1.4; margin: 0; }

.chart-card {
  background: white;
  border-radius: var(--radius-md);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
}

.chart-title {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 16px;
}

/* Barras */
.bar-chart { display: flex; flex-direction: column; gap: 10px; }

.bar-row {
  display: grid;
  grid-template-columns: 220px 1fr 36px;
  align-items: center;
  gap: 10px;
}

.bar-name { font-size: 0.78rem; color: var(--color-text); font-weight: 500; }

.bar-track {
  height: 10px;
  background: var(--color-bg);
  border-radius: 6px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--color-primary), var(--color-secondary));
  border-radius: 6px;
  transition: width 0.6s ease;
}

.bar-count { font-size: 0.78rem; font-weight: 700; color: var(--color-primary); text-align: right; }

/* Dona */
.chart-small { max-width: 340px; }

.dona-wrap {
  position: relative;
  width: 140px;
  margin: 0 auto 12px;
}

.dona-svg { width: 100%; }

.dona-center {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}

.dona-pct {
  font-family: var(--font-display);
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.dona-sub { font-size: 0.65rem; color: var(--color-muted); margin: 0; }

.dona-leyenda { display: flex; flex-direction: column; gap: 5px; }

.leyenda-item { font-size: 0.8rem; color: var(--color-text); display: flex; align-items: center; gap: 6px; }

.leyenda-dot { width: 10px; height: 10px; border-radius: 50%; display: inline-block; }
.dot-urgent { background: #e65100; }
.dot-normal { background: var(--color-primary); }

/* Línea */
.chart-wide { }
.line-chart-wrap { width: 100%; overflow-x: auto; }
.line-svg { width: 100%; min-width: 300px; }

/* ── Leads table ─────────────────────────────────────────────── */
.leads-toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}

.search-input {
  flex: 1;
  min-width: 200px;
  padding: 9px 14px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-family: var(--font-body);
  outline: none;
  transition: border-color var(--transition);
}
.search-input:focus { border-color: var(--color-primary); }

.filter-select {
  padding: 9px 12px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-size: 0.88rem;
  font-family: var(--font-body);
  background: white;
  cursor: pointer;
  outline: none;
}

.leads-table-wrap { overflow-x: auto; }

.leads-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.82rem;
  background: white;
  border-radius: var(--radius-md);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.leads-table th {
  background: var(--color-dark);
  color: white;
  padding: 11px 12px;
  text-align: left;
  font-weight: 700;
  font-size: 0.72rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.leads-table td {
  padding: 10px 12px;
  border-bottom: 1px solid var(--color-border);
  color: var(--color-text);
  vertical-align: middle;
}

.leads-table tr:last-child td { border-bottom: none; }
.leads-table tr:hover td { background: var(--color-bg); }

.td-fecha { white-space: nowrap; color: var(--color-muted); font-size: 0.75rem; }
.td-bold  { font-weight: 600; }

.badge-servicio {
  font-size: 0.7rem;
  font-weight: 600;
  background: #e8f5e9;
  color: var(--color-primary-dark);
  padding: 2px 8px;
  border-radius: 20px;
  white-space: nowrap;
}

.badge-urgencia {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 2px 8px;
  border-radius: 20px;
  white-space: nowrap;
}
.badge-urgencia.urgent { background: #fff3e0; color: #e65100; }
.badge-urgencia.normal { background: #e8f5e9; color: var(--color-primary-dark); }

.badge-estado {
  font-size: 0.68rem;
  font-weight: 600;
  background: var(--color-bg);
  color: var(--color-muted);
  padding: 2px 7px;
  border-radius: 20px;
  border: 1px solid var(--color-border);
}

/* ── Historial ───────────────────────────────────────────────── */
.historial-layout {
  display: grid;
  grid-template-columns: 260px 1fr;
  gap: 20px;
  height: 600px;
}

.sesiones-list {
  background: white;
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-y: auto;
  box-shadow: var(--shadow-sm);
}

.section-label {
  font-family: var(--font-display);
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0 0 12px;
}

.sesion-item {
  padding: 10px 12px;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all var(--transition);
  border-left: 3px solid transparent;
  margin-bottom: 4px;
}

.sesion-item:hover { background: var(--color-bg); border-left-color: var(--color-primary); }
.sesion-item.active { background: #e8f5e9; border-left-color: var(--color-primary); }

.sesion-id { font-size: 0.8rem; font-weight: 600; color: var(--color-text); font-family: monospace; }
.sesion-meta { font-size: 0.7rem; color: var(--color-muted); margin-top: 2px; }

.historial-detalle {
  background: white;
  border-radius: var(--radius-md);
  padding: 16px;
  overflow-y: auto;
  box-shadow: var(--shadow-sm);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.historial-msgs { display: flex; flex-direction: column; gap: 10px; }

.hm-row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
}

.hm-row.user { flex-direction: row-reverse; }

.hm-avatar {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  flex-shrink: 0;
  background: var(--color-bg);
}

.hm-bubble {
  max-width: 70%;
  padding: 8px 12px;
  border-radius: 12px;
}

.hm-row.assistant .hm-bubble { background: var(--color-bg); border-bottom-left-radius: 3px; }
.hm-row.user .hm-bubble      { background: var(--color-dark); color: white; border-bottom-right-radius: 3px; }

.hm-content { font-size: 0.82rem; line-height: 1.5; margin: 0; }
.hm-time    { font-size: 0.65rem; opacity: 0.5; display: block; margin-top: 3px; text-align: right; }

/* ── Generales ───────────────────────────────────────────────── */
.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--color-muted);
  font-size: 0.92rem;
  background: white;
  border-radius: var(--radius-md);
}

.empty-state.small { padding: 16px; font-size: 0.8rem; }

.tab-content { animation: fadeUp 0.25s ease both; }

@media (max-width: 768px) {
  .historial-layout { grid-template-columns: 1fr; height: auto; }
  .kpi-row { grid-template-columns: 1fr; }
  .bar-row { grid-template-columns: 1fr 80px; }
  .bar-name { grid-column: 1 / -1; }
}
</style>