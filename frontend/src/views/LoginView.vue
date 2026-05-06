<template>
  <div class="login-page">
    <div class="login-card">
      <!-- Logo / marca -->
      <div class="login-brand">
        <span class="brand-leaf">🌿</span>
        <div>
          <p class="brand-name">Biótica Consultores</p>
          <p class="brand-sub">Panel de Administración</p>
        </div>
      </div>

      <h2 class="login-title">Iniciar sesión</h2>
      <p class="login-desc">Accede para gestionar leads e indicadores.</p>

      <!-- Error -->
      <div v-if="error" class="login-error">
        <span>⚠️ {{ error }}</span>
      </div>

      <!-- Formulario -->
      <div class="login-form">
        <div class="field">
          <label class="field-label">Usuario</label>
          <input
            v-model="usuario"
            class="field-input"
            type="text"
            placeholder="admin"
            @keydown.enter="login"
            autocomplete="username"
          />
        </div>

        <div class="field">
          <label class="field-label">Contraseña</label>
          <div class="pw-wrap">
            <input
              v-model="password"
              class="field-input"
              :type="showPw ? 'text' : 'password'"
              placeholder="••••••••"
              @keydown.enter="login"
              autocomplete="current-password"
            />
            <button class="pw-toggle" @click="showPw = !showPw" type="button">
              {{ showPw ? '🙈' : '👁️' }}
            </button>
          </div>
        </div>

        <button
          class="login-btn"
          :class="{ loading: cargando }"
          :disabled="cargando || !usuario || !password"
          @click="login"
        >
          <span v-if="!cargando">Entrar al panel →</span>
          <span v-else>Verificando...</span>
        </button>
      </div>

      <router-link to="/" class="back-link">← Volver al sitio</router-link>
    </div>
  </div>
</template>

<script>
import { mapGetters, mapActions } from 'vuex'

export default {
  name: 'LoginView',
  data() {
    return { usuario: '', password: '', showPw: false, cargando: false }
  },
  computed: {
    ...mapGetters(['adminError']),
    error() { return this.adminError }
  },
  methods: {
    ...mapActions(['adminLogin']),
    async login() {
      if (!this.usuario || !this.password) return
      this.cargando = true
      const ok = await this.adminLogin({ usuario: this.usuario, password: this.password })
      this.cargando = false
      if (ok) {
        const redirect = this.$route.query.redirect || '/admin'
        this.$router.push(redirect)
      }
    }
  }
}
</script>

<style scoped>
.login-page {
  min-height: calc(100vh - 64px);
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-dark-ultra) 0%, var(--color-dark) 100%);
  padding: 2rem;
}

.login-card {
  background: var(--color-white);
  border-radius: var(--radius-lg);
  padding: 2.5rem;
  width: 100%;
  max-width: 400px;
  box-shadow: var(--shadow-lg);
  animation: fadeUp 0.4s ease both;
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}

.login-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border);
}

.brand-leaf { font-size: 2rem; }

.brand-name {
  font-family: var(--font-display);
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-primary);
  margin: 0;
}

.brand-sub {
  font-size: 0.72rem;
  color: var(--color-muted);
  margin: 0;
}

.login-title {
  font-family: var(--font-display);
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text);
  margin: 0;
}

.login-desc {
  font-size: 0.85rem;
  color: var(--color-muted);
  margin: -0.6rem 0 0;
}

.login-error {
  background: #fff3f3;
  border: 1px solid #f5c2c2;
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  font-size: 0.85rem;
  color: #c0392b;
}

.login-form { display: flex; flex-direction: column; gap: 1rem; }

.field { display: flex; flex-direction: column; gap: 5px; }

.field-label {
  font-size: 0.78rem;
  font-weight: 700;
  color: var(--color-text);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.field-input {
  width: 100%;
  padding: 10px 14px;
  border: 2px solid var(--color-border);
  border-radius: var(--radius-sm);
  font-family: var(--font-body);
  font-size: 0.92rem;
  color: var(--color-text);
  background: var(--color-bg);
  transition: border-color var(--transition), box-shadow var(--transition);
  outline: none;
}

.field-input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(84,180,53,0.12);
  background: #fff;
}

.pw-wrap { position: relative; }
.pw-wrap .field-input { padding-right: 44px; }

.pw-toggle {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background: var(--color-primary);
  color: white;
  font-family: var(--font-body);
  font-size: 0.95rem;
  font-weight: 700;
  border-radius: var(--radius-sm);
  border: none;
  cursor: pointer;
  transition: all var(--transition);
  box-shadow: 0 3px 12px rgba(84,180,53,0.3);
}

.login-btn:hover:not(:disabled) {
  background: var(--color-primary-light);
  transform: translateY(-1px);
}

.login-btn:disabled { opacity: 0.55; cursor: not-allowed; }

.login-btn.loading {
  background: var(--color-secondary);
  cursor: wait;
}

.back-link {
  font-size: 0.8rem;
  color: var(--color-muted);
  text-align: center;
  text-decoration: none;
  transition: color var(--transition);
}
.back-link:hover { color: var(--color-primary); }
</style>