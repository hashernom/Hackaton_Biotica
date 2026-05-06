import api from './api'

const adminService = {
  // ── Auth ──────────────────────────────────────────────────────────
  async login(usuario, password) {
    return await api.post('/admin/login', { usuario, password })
  },

  async logout(token) {
    return await api.post('/admin/logout', {}, {
      headers: { Authorization: `Bearer ${token}` }
    })
  },

  // ── Leads ─────────────────────────────────────────────────────────
  async getLeads(token, urgencia = null) {
    const params = urgencia ? { urgencia } : {}
    return await api.get('/admin/leads', {
      headers: { Authorization: `Bearer ${token}` },
      params,
    })
  },

  // ── Estadísticas ──────────────────────────────────────────────────
  async getStats(token) {
    return await api.get('/admin/stats', {
      headers: { Authorization: `Bearer ${token}` }
    })
  },

  // ── Sesiones / Historial ──────────────────────────────────────────
  async getSesiones(token) {
    return await api.get('/admin/sesiones', {
      headers: { Authorization: `Bearer ${token}` }
    })
  },

  async getHistorial(token, sessionId) {
    return await api.get(`/admin/sesiones/${sessionId}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
  },

  // ── Exportación ───────────────────────────────────────────────────
  async exportarExcel(token) {
    const res = await api.get('/admin/export/excel', {
      headers:      { Authorization: `Bearer ${token}` },
      responseType: 'blob',
    })
    _descargarBlob(res, `biotica_leads_${_timestamp()}.xlsx`)
  },

  async exportarCSV(token) {
    const res = await api.get('/admin/export/csv', {
      headers:      { Authorization: `Bearer ${token}` },
      responseType: 'blob',
    })
    _descargarBlob(res, `biotica_leads_${_timestamp()}.csv`)
  },
}

// ── Helpers ─────────────────────────────────────────────────────────────────
function _descargarBlob(blob, filename) {
  const url  = URL.createObjectURL(blob)
  const link = document.createElement('a')
  link.href     = url
  link.download = filename
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}

function _timestamp() {
  return new Date().toISOString().slice(0, 16).replace('T', '_').replace(':', '')
}

export default adminService