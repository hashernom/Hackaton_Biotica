import { createStore } from 'vuex'
import chatService  from '../services/chat.service'
import adminService from '../services/admin.service'
import { WELCOME_MESSAGE } from '../utils/constants'

export default createStore({
  state: {
    // ── Chat ──────────────────────────────────────────────────────────
    messages:  [],
    isLoading: false,
    sessionId: null,
    leadData: {
      nombre: 'N/A', contacto: 'N/A',
      proyecto: 'N/A', ubicacion: 'N/A',
      clasificacion: null, urgencia: null,
      finalizado: false, info_tecnica: ''
    },

    // ── Admin ─────────────────────────────────────────────────────────
    adminToken:   null,
    adminUsuario: null,
    adminLeads:   [],
    adminMetricas: null,
    adminStats:    null,
    adminSesiones: [],
    adminHistorial: null,   // { session_id, mensajes }
    adminLoading:  false,
    adminError:    null,
  },

  getters: {
    messages:        s => s.messages,
    isLoading:       s => s.isLoading,
    leadData:        s => s.leadData,
    isLeadFinalizado:s => s.leadData.finalizado,
    isUrgente:       s => s.leadData.urgencia === 'Alta',
    sessionId:       s => s.sessionId,

    isAdminLoggedIn: s => !!s.adminToken,
    adminToken:      s => s.adminToken,
    adminUsuario:    s => s.adminUsuario,
    adminLeads:      s => s.adminLeads,
    adminMetricas:   s => s.adminMetricas,
    adminStats:      s => s.adminStats,
    adminSesiones:   s => s.adminSesiones,
    adminHistorial:  s => s.adminHistorial,
    adminLoading:    s => s.adminLoading,
    adminError:      s => s.adminError,
  },

  mutations: {
    // ── Chat ────────────────────────────────────────────────────────
    ADD_MESSAGE(state, msg) { state.messages.push(msg) },
    SET_LOADING(state, v)   { state.isLoading = v },
    SET_SESSION(state, id)  { state.sessionId = id },

    UPDATE_LEAD(state, data) {
      if (data.lead_actualizado) {
        const la = data.lead_actualizado
        if (la.nombre   && la.nombre   !== 'N/A') state.leadData.nombre   = la.nombre
        if (la.contacto && la.contacto !== 'N/A') state.leadData.contacto = la.contacto
        if (la.proyecto && la.proyecto !== 'N/A') state.leadData.proyecto = la.proyecto
        if (la.ubicacion&& la.ubicacion!== 'N/A') state.leadData.ubicacion= la.ubicacion
        if (la.info_tecnica) state.leadData.info_tecnica = la.info_tecnica
      }
      if (data.clasificacion) state.leadData.clasificacion = data.clasificacion
      if (data.urgencia)      state.leadData.urgencia      = data.urgencia
      if (data.es_finalizado) state.leadData.finalizado    = true
      if (data.session_id)    state.sessionId              = data.session_id
    },

    CLEAR_CHAT(state) {
      state.messages  = []
      state.sessionId = null
      state.leadData  = {
        nombre: 'N/A', contacto: 'N/A', proyecto: 'N/A',
        ubicacion: 'N/A', clasificacion: null, urgencia: null,
        finalizado: false, info_tecnica: ''
      }
    },

    // ── Admin ────────────────────────────────────────────────────────
    SET_ADMIN_AUTH(state, { token, usuario }) {
      state.adminToken   = token
      state.adminUsuario = usuario
    },
    CLEAR_ADMIN_AUTH(state) {
      state.adminToken   = null
      state.adminUsuario = null
    },
    SET_ADMIN_LEADS(state, { leads, metricas }) {
      state.adminLeads    = leads
      state.adminMetricas = metricas
    },
    SET_ADMIN_STATS(state, stats)       { state.adminStats    = stats },
    SET_ADMIN_SESIONES(state, sesiones) { state.adminSesiones = sesiones },
    SET_ADMIN_HISTORIAL(state, data)    { state.adminHistorial = data },
    SET_ADMIN_LOADING(state, v)         { state.adminLoading  = v },
    SET_ADMIN_ERROR(state, msg)         { state.adminError    = msg },
  },

  actions: {
    // ── Chat ────────────────────────────────────────────────────────
    initChat({ commit, state }) {
      if (state.messages.length === 0) {
        commit('ADD_MESSAGE', { ...WELCOME_MESSAGE, ts: Date.now() })
      }
    },

    async sendMessage({ commit, state }, userText) {
      commit('ADD_MESSAGE', { role: 'user', content: userText, ts: Date.now() })
      commit('SET_LOADING', true)
      try {
        const history = state.messages.map(m => ({ role: m.role, content: m.content }))
        const res = await chatService.enviarMensaje(
          history,
          state.leadData,
          state.sessionId
        )
        commit('UPDATE_LEAD', res)
        commit('ADD_MESSAGE', {
          role: 'assistant',
          content: res.respuesta_bot,
          ts: Date.now(),
          meta: {
            clasificacion: res.clasificacion,
            urgencia:      res.urgencia,
            finalizado:    res.es_finalizado,
            tiempo_ms:     res.tiempo_respuesta_ms,
          }
        })
      } catch (err) {
        commit('ADD_MESSAGE', {
          role: 'assistant',
          content: 'Lo siento, tuve un problema de conexión. ¿Podrías repetir?',
          ts: Date.now(), error: true
        })
      } finally {
        commit('SET_LOADING', false)
      }
    },

    resetChat({ commit }) { commit('CLEAR_CHAT') },

    // ── Admin ────────────────────────────────────────────────────────
    async adminLogin({ commit }, { usuario, password }) {
      commit('SET_ADMIN_ERROR', null)
      try {
        const res = await adminService.login(usuario, password)
        commit('SET_ADMIN_AUTH', { token: res.token, usuario: res.usuario })
        // Persiste token en sessionStorage para recargas
        sessionStorage.setItem('biotica_token',   res.token)
        sessionStorage.setItem('biotica_usuario',  res.usuario)
        return true
      } catch (e) {
        commit('SET_ADMIN_ERROR', e.message || 'Credenciales incorrectas')
        return false
      }
    },

    async adminLogout({ commit, state }) {
      try { await adminService.logout(state.adminToken) } catch (e) { console.warn('Logout:', e) }
      commit('CLEAR_ADMIN_AUTH')
      sessionStorage.removeItem('biotica_token')
      sessionStorage.removeItem('biotica_usuario')
    },

    restoreAdminSession({ commit }) {
      const token   = sessionStorage.getItem('biotica_token')
      const usuario = sessionStorage.getItem('biotica_usuario')
      if (token && usuario) commit('SET_ADMIN_AUTH', { token, usuario })
    },

    async fetchLeads({ commit, state }) {
      commit('SET_ADMIN_LOADING', true)
      try {
        const res = await adminService.getLeads(state.adminToken)
        commit('SET_ADMIN_LEADS', { leads: res.leads, metricas: res.metricas })
      } catch (e) {
        commit('SET_ADMIN_ERROR', e.message)
      } finally {
        commit('SET_ADMIN_LOADING', false)
      }
    },

    async fetchStats({ commit, state }) {
      try {
        const res = await adminService.getStats(state.adminToken)
        commit('SET_ADMIN_STATS', res)
      } catch (e) {
        commit('SET_ADMIN_ERROR', e.message)
      }
    },

    async fetchSesiones({ commit, state }) {
      try {
        const res = await adminService.getSesiones(state.adminToken)
        commit('SET_ADMIN_SESIONES', res.sesiones)
      } catch (e) {
        commit('SET_ADMIN_ERROR', e.message)
      }
    },

    async fetchHistorial({ commit, state }, sessionId) {
      try {
        const res = await adminService.getHistorial(state.adminToken, sessionId)
        commit('SET_ADMIN_HISTORIAL', res)
      } catch (e) {
        commit('SET_ADMIN_ERROR', e.message)
      }
    },
  }
})