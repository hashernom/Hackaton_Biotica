import api from './api'

const chatService = {
  async enviarMensaje(historial, leadTemp = null, sessionId = null) {
    return await api.post('/chat', {
      messages:   historial,
      lead_temp:  leadTemp,
      session_id: sessionId,
    })
  }
}

export default chatService