<template>
  <div id="app-root">
    <AppHeader />
    <main class="main-content">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from './components/layout/AppHeader.vue'
import AppFooter from './components/layout/AppFooter.vue'
import { mapActions } from 'vuex'

export default {
  name: 'App',
  components: { AppHeader, AppFooter },
  created() {
    // Restaura sesión admin si hay token guardado en sessionStorage
    this.restoreAdminSession()
  },
  methods: {
    ...mapActions(['restoreAdminSession'])
  }
}
</script>

<style>
#app-root {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}
.fade-enter-active,
.fade-leave-active { transition: opacity 0.22s ease, transform 0.22s ease; }
.fade-enter-from   { opacity: 0; transform: translateY(8px); }
.fade-leave-to     { opacity: 0; transform: translateY(-4px); }
</style>