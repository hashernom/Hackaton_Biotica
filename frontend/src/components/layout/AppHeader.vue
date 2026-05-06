<template>
  <header class="app-header">
    <div class="header-inner container">
      <router-link to="/" class="logo-link">
        <img
          src="@/assets/images/LogoBioTech.png"
          alt="Biótica Consultores"
          class="logo-img"
          onerror="this.style.display='none';this.nextElementSibling.style.display='flex'"
        />
        <span class="logo-fallback" style="display:none">
          <span class="logo-leaf">🌿</span>
          <span class="logo-name">Biótica</span>
        </span>
      </router-link>

      <nav class="header-nav">
        <router-link to="/"    class="nav-link" :class="{ active: $route.name==='home' }">Inicio</router-link>
        <router-link to="/chat" class="nav-link nav-cta" :class="{ active: $route.name==='chat' }">
          💬 Asistente
        </router-link>
        <router-link v-if="isAdminLoggedIn" to="/admin" class="nav-link nav-admin" :class="{ active: $route.name==='admin' }">
          📊 Admin
        </router-link>
        <router-link v-else to="/login" class="nav-link nav-admin-out" :class="{ active: $route.name==='login' }">
          🔐 Admin
        </router-link>
      </nav>
    </div>
  </header>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  name: 'AppHeader',
  computed: { ...mapGetters(['isAdminLoggedIn']) }
}
</script>

<style scoped>
.app-header {
  background: var(--color-dark);
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 2px 16px rgba(30,46,33,0.22);
}
.header-inner {
  display: flex; align-items: center;
  justify-content: space-between; height: 64px;
}
.logo-link { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo-img   { height: 38px; width: auto; object-fit: contain; }
.logo-fallback { display: flex; align-items: center; gap: 8px; }
.logo-leaf  { font-size: 1.5rem; }
.logo-name  { font-family: var(--font-display); font-size: 1.35rem; font-weight: 700; color: var(--color-primary); }
.header-nav { display: flex; align-items: center; gap: 6px; }
.nav-link {
  font-size: 0.88rem; font-weight: 500;
  color: rgba(255,255,255,0.7);
  padding: 7px 16px; border-radius: var(--radius-xl);
  transition: all var(--transition); text-decoration: none;
}
.nav-link:hover, .nav-link.active { color: white; background: rgba(84,180,53,0.15); }
.nav-cta { background: var(--color-primary); color: white !important; }
.nav-cta:hover { background: var(--color-primary-light) !important; transform: translateY(-1px); }
.nav-admin { background: rgba(84,180,53,0.2); color: var(--color-primary) !important; }
.nav-admin:hover { background: rgba(84,180,53,0.3) !important; }
.nav-admin-out { border: 1px solid rgba(255,255,255,0.2); }
</style>