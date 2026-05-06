<template>
  <footer class="app-footer">
    <div class="container footer-inner">
      <div class="footer-brand">
        <span class="footer-logo">🌿 Biótica Consultores</span>
        <p class="footer-tagline">Nuestro negocio es la conservación</p>
      </div>
      <div class="footer-links">
        <a href="https://bioticaconsultores.com/" target="_blank" rel="noopener">Web oficial</a>
        <span class="sep">·</span>
        <span>Floridablanca, Santander · Colombia</span>
      </div>
      <p class="footer-copy">© {{ year }} Biótica Consultores LTDA. Todos los derechos reservados.</p>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'AppFooter',
  computed: {
    year() { return new Date().getFullYear() }
  }
}
</script>

<style scoped>
.app-footer {
  background: var(--color-dark-ultra);
  color: rgba(255,255,255,0.55);
  padding: 2rem 0 1.5rem;
  margin-top: auto;
}

.footer-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  text-align: center;
}

.footer-logo {
  font-family: var(--font-display);
  font-size: 1.1rem;
  color: var(--color-primary);
  font-weight: 700;
}

.footer-tagline {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.4);
  margin-top: 2px;
}

.footer-links {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.82rem;
}

.footer-links a {
  color: var(--color-secondary);
  transition: color var(--transition);
}
.footer-links a:hover { color: var(--color-primary); }

.sep { color: rgba(255,255,255,0.25); }

.footer-copy {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.25);
  margin-top: 0.5rem;
}
</style>