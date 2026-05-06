<template>
  <div class="home">
    <!-- Hero -->
    <section class="hero">
      <div class="hero-bg-shapes">
        <div class="shape shape-1" />
        <div class="shape shape-2" />
        <div class="shape shape-3" />
      </div>
      <div class="container hero-inner">
        <div class="hero-text">
          <span class="hero-eyebrow">🌿 Consultoría Ambiental con IA</span>
          <h1 class="hero-title">
            Nuestro negocio<br />
            <em>es la conservación</em>
          </h1>
          <p class="hero-desc">
            Biótica Consultores lleva más de 15 años liderando la gestión de recursos naturales
            en Colombia. Ahora con nuestro asistente inteligente, obtén atención inmediata
            para tu proyecto ambiental.
          </p>
          <div class="hero-ctas">
            <router-link to="/chat" class="btn-primary">
              💬 Iniciar consulta
            </router-link>
            <a href="https://bioticaconsultores.com/" target="_blank" rel="noopener" class="btn-outline">
              Conocer más →
            </a>
          </div>
        </div>
        <div class="hero-visual">
          <div class="visual-card">
            <div class="vc-header">
              <span class="vc-dot green" /><span class="vc-dot yellow" /><span class="vc-dot red" />
              <span class="vc-title">AsistenteBiótica</span>
            </div>
            <div class="vc-chat">
              <div class="vc-msg bot">
                <span class="vc-avatar">🌿</span>
                <span class="vc-bubble">¡Hola! ¿En qué proyecto ambiental puedo ayudarte?</span>
              </div>
              <div class="vc-msg user">
                <span class="vc-bubble">Necesito una licencia ambiental urgente</span>
                <span class="vc-avatar">👤</span>
              </div>
              <div class="vc-msg bot">
                <span class="vc-avatar">🌿</span>
                <span class="vc-bubble">Entendido 🔥 Caso de prioridad alta. ¿Me compartes tu nombre y contacto?</span>
              </div>
              <div class="vc-typing">
                <span /><span /><span />
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Servicios -->
    <section class="servicios-section">
      <div class="container">
        <h2 class="section-title">Nuestros Servicios</h2>
        <p class="section-sub">Clasificados automáticamente por nuestra IA para conectarte con el experto correcto</p>
        <div class="servicios-grid">
          <div
            class="servicio-card"
            v-for="s in servicios"
            :key="s.nombre"
            @click="goChat(s.nombre)"
          >
            <span class="s-icon">{{ s.icon }}</span>
            <span class="s-name">{{ s.nombre }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Stats / Atributos -->
    <section class="stats-section">
      <div class="container stats-grid">
        <div class="stat-card" v-for="st in stats" :key="st.label">
          <span class="stat-value">{{ st.value }}</span>
          <span class="stat-label">{{ st.label }}</span>
        </div>
      </div>
    </section>

    <!-- CTA final -->
    <section class="cta-section">
      <div class="container cta-inner">
        <h2 class="cta-title">¿Listo para optimizar tu gestión ambiental?</h2>
        <p class="cta-desc">Nuestro asistente con IA atiende tu solicitud en menos de 5 segundos y la envía al consultor correcto.</p>
        <router-link to="/chat" class="btn-primary btn-lg">
          Iniciar consulta ahora 🚀
        </router-link>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  name: 'HomeView',
  data() {
    return {
      servicios: [
        { icon: '🦜', nombre: 'Monitoreo de Fauna y Flora' },
        { icon: '🌲', nombre: 'Aprovechamiento Forestal (PAF)' },
        { icon: '📋', nombre: 'Plan de Manejo Ambiental (PMA)' },
        { icon: '📄', nombre: 'Estudio de Impacto Ambiental (EIA)' },
        { icon: '🗺️', nombre: 'Ordenamiento Territorial' },
        { icon: '🌱', nombre: 'Restauración Ecológica' },
        { icon: '🏕️', nombre: 'Ecoturismo y Educación Ambiental' },
        { icon: '♻️', nombre: 'Consultoría en Sostenibilidad' },
        { icon: '🔬', nombre: 'Suministro de Equipos Ambientales' }
      ],
      stats: [
        { value: '+15', label: 'Años de experiencia' },
        { value: '< 5s', label: 'Tiempo de respuesta IA' },
        { value: '9', label: 'Líneas de servicio' },
        { value: '24/7', label: 'Disponibilidad del asistente' }
      ]
    }
  },
  methods: {
    goChat(servicio) {
      this.$router.push({ name: 'chat', query: { servicio } })
    }
  }
}
</script>

<style scoped>
/* ── Hero ─────────────────────────────────── */
.hero {
  position: relative;
  background: var(--color-dark);
  overflow: hidden;
  padding: 80px 0 90px;
}

.hero-bg-shapes {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.shape {
  position: absolute;
  border-radius: 50%;
  opacity: 0.08;
}

.shape-1 {
  width: 520px; height: 520px;
  background: var(--color-primary);
  top: -180px; right: -120px;
}
.shape-2 {
  width: 300px; height: 300px;
  background: var(--color-secondary);
  bottom: -100px; left: -80px;
}
.shape-3 {
  width: 180px; height: 180px;
  background: var(--color-primary);
  top: 40%; left: 38%;
}

.hero-inner {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 60px;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-eyebrow {
  display: inline-block;
  font-size: 0.78rem;
  font-weight: 700;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--color-primary);
  background: rgba(84,180,53,0.12);
  border: 1px solid rgba(84,180,53,0.25);
  padding: 4px 14px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.hero-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 4vw, 3.2rem);
  font-weight: 700;
  color: var(--color-white);
  line-height: 1.18;
  margin-bottom: 18px;
}

.hero-title em {
  font-style: italic;
  color: var(--color-primary);
}

.hero-desc {
  font-size: 1rem;
  line-height: 1.7;
  color: rgba(255,255,255,0.65);
  margin-bottom: 32px;
  max-width: 480px;
}

.hero-ctas {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: var(--color-primary);
  color: white;
  font-weight: 700;
  font-size: 0.92rem;
  padding: 12px 26px;
  border-radius: var(--radius-xl);
  text-decoration: none;
  transition: all var(--transition);
  box-shadow: 0 4px 16px rgba(84,180,53,0.35);
}

.btn-primary:hover {
  background: var(--color-primary-light);
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(84,180,53,0.4);
}

.btn-lg { padding: 15px 36px; font-size: 1rem; }

.btn-outline {
  display: inline-flex;
  align-items: center;
  font-weight: 600;
  font-size: 0.92rem;
  padding: 12px 22px;
  border-radius: var(--radius-xl);
  border: 1.5px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.8);
  text-decoration: none;
  transition: all var(--transition);
}

.btn-outline:hover {
  border-color: rgba(255,255,255,0.5);
  color: white;
  background: rgba(255,255,255,0.06);
}

/* ── Visual card (chat preview) ───────────── */
.hero-visual {
  display: flex;
  justify-content: center;
}

.visual-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-lg);
  overflow: hidden;
  width: 100%;
  max-width: 380px;
  animation: fadeUp 0.7s ease 0.2s both;
}

.vc-header {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 12px 16px;
  background: var(--color-dark);
  border-bottom: 1px solid rgba(255,255,255,0.08);
}

.vc-dot {
  width: 10px; height: 10px;
  border-radius: 50%;
}
.vc-dot.green  { background: var(--color-primary); }
.vc-dot.yellow { background: var(--color-secondary); }
.vc-dot.red    { background: #e55; }

.vc-title {
  font-size: 0.75rem;
  font-weight: 700;
  color: rgba(255,255,255,0.6);
  margin-left: 6px;
  font-family: var(--font-body);
}

.vc-chat {
  padding: 16px;
  background: var(--chat-area-bg);
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 200px;
}

.vc-msg {
  display: flex;
  align-items: flex-end;
  gap: 8px;
}

.vc-msg.user { flex-direction: row-reverse; }

.vc-avatar {
  width: 28px; height: 28px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.85rem;
  flex-shrink: 0;
}

.vc-msg.bot .vc-avatar  { background: var(--color-primary); }
.vc-msg.user .vc-avatar { background: var(--color-dark); }

.vc-bubble {
  font-size: 0.78rem;
  line-height: 1.5;
  padding: 8px 12px;
  border-radius: 12px;
  max-width: 75%;
}

.vc-msg.bot .vc-bubble  { background: white; color: var(--color-text); border-bottom-left-radius: 3px; }
.vc-msg.user .vc-bubble { background: var(--color-dark); color: white; border-bottom-right-radius: 3px; }

.vc-typing {
  display: flex;
  gap: 4px;
  padding: 10px 14px;
  background: white;
  border-radius: 12px;
  width: fit-content;
  border-bottom-left-radius: 3px;
  margin-left: 36px;
}

.vc-typing span {
  width: 7px; height: 7px;
  border-radius: 50%;
  background: var(--color-primary);
  animation: pulse 1.2s infinite;
}
.vc-typing span:nth-child(2) { animation-delay: 0.2s; background: var(--color-secondary); }
.vc-typing span:nth-child(3) { animation-delay: 0.4s; background: var(--color-dark); }

/* ── Servicios ────────────────────────────── */
.servicios-section {
  padding: 80px 0;
  background: var(--color-bg);
}

.section-title {
  font-family: var(--font-display);
  font-size: clamp(1.6rem, 3vw, 2.2rem);
  font-weight: 700;
  color: var(--color-text);
  text-align: center;
  margin-bottom: 8px;
}

.section-sub {
  text-align: center;
  color: var(--color-muted);
  font-size: 0.95rem;
  margin-bottom: 44px;
}

.servicios-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 14px;
}

.servicio-card {
  background: var(--color-white);
  border: 1.5px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: 20px 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: all var(--transition);
  text-align: center;
}

.servicio-card:hover {
  border-color: var(--color-primary);
  box-shadow: var(--shadow-md);
  transform: translateY(-3px);
  background: linear-gradient(135deg, #f4faf0, #fff);
}

.s-icon {
  font-size: 2rem;
  line-height: 1;
}

.s-name {
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--color-text);
  line-height: 1.3;
}

/* ── Stats ────────────────────────────────── */
.stats-section {
  background: linear-gradient(135deg, var(--color-dark), var(--color-dark-light));
  padding: 60px 0;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.stat-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
}

.stat-value {
  font-family: var(--font-display);
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  line-height: 1;
}

.stat-label {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.55);
  text-align: center;
  font-weight: 500;
}

/* ── CTA ──────────────────────────────────── */
.cta-section {
  background: var(--color-bg);
  padding: 80px 0;
}

.cta-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 16px;
}

.cta-title {
  font-family: var(--font-display);
  font-size: clamp(1.5rem, 3vw, 2.2rem);
  font-weight: 700;
  color: var(--color-text);
  max-width: 600px;
}

.cta-desc {
  font-size: 1rem;
  color: var(--color-muted);
  max-width: 500px;
  line-height: 1.7;
  margin-bottom: 8px;
}

/* ── Responsive ───────────────────────────── */
@media (max-width: 900px) {
  .hero-inner {
    grid-template-columns: 1fr;
    gap: 40px;
    text-align: center;
  }
  .hero-desc { max-width: 100%; }
  .hero-ctas { justify-content: center; }

  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
  }
}

@media (max-width: 560px) {
  .servicios-grid { grid-template-columns: 1fr 1fr; }
  .stats-grid { grid-template-columns: 1fr 1fr; }
}
</style>