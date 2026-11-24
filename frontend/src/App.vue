<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { Activity, BookOpen, ChevronRight, CircleHelp, ClipboardList, Code2, Compass, FlaskConical, Github, Grid3X3, Home, Menu, Moon, Radar, ScanSearch, Shield, ShieldAlert, Sun, X } from 'lucide-vue-next'
import { loadError, loading, refresh, showcase } from './api'

const groups = [
  { name: 'Learning', items: [
    { text: 'Start Here', path: '/', icon: Home }, { text: 'Learn', path: '/learn', icon: BookOpen },
    { text: 'Technique Explorer', path: '/techniques', icon: Compass }, { text: 'Simulate', path: '/simulate', icon: FlaskConical },
  ] },
  { name: 'Investigate', items: [
    { text: 'Alerts', path: '/alerts', icon: ShieldAlert }, { text: 'Hunt Workspace', path: '/hunt', icon: ScanSearch },
    { text: 'ATT&CK Matrix', path: '/matrix', icon: Grid3X3 }, { text: 'Investigations', path: '/investigations', icon: ClipboardList },
    { text: 'Detection Rules', path: '/rules', icon: Code2 }, { text: 'Playbooks', path: '/playbooks', icon: Shield },
  ] },
  { name: 'Resources', items: [
    { text: 'Learning Progress', path: '/progress', icon: Activity }, { text: 'Deployment Help', path: '/deployment', icon: CircleHelp },
    { text: 'About / Contribute', path: '/about', icon: Github },
  ] },
]
const route = useRoute()
const menu = ref(false)
const theme = ref('dark')
const main = ref<HTMLElement>()
const pageName = computed(() => route.meta.title ?? 'Start Here')
function setTheme(value: string) {
  theme.value = value
  document.documentElement.dataset.theme = value
  try { localStorage.setItem('threathuntx.theme', value) } catch { /* theme still applies */ }
}
watch(() => route.path, () => {
  menu.value = false
  main.value?.focus({ preventScroll: true })
})
watch(pageName, value => { document.title = `${String(value)} · ThreatHuntX` }, { immediate: true })
onMounted(() => {
  try { if (localStorage.getItem('threathuntx.theme') === 'light') setTheme('light') } catch { /* use default */ }
  void refresh()
})
</script>

<template>
  <a class="skip-link" href="#main-content" @click.prevent="main?.focus()">Skip to content</a>
  <div class="shell" @keydown.esc="menu = false">
    <aside id="workspace-navigation" class="sidebar" :class="{ 'mobile-open': menu }">
      <RouterLink class="brand" to="/"><span class="brand-icon"><Radar :size="23" aria-hidden="true" /></span><span><strong>ThreatHunt<span>X</span></strong><small>{{ showcase ? 'PUBLIC SHOWCASE' : 'COMMUNITY LAB' }}</small></span></RouterLink>
      <nav class="side-nav" aria-label="Main navigation">
        <div v-for="group in groups" :key="group.name" class="nav-group"><p>{{ group.name }}</p>
          <RouterLink v-for="item in group.items" :key="item.path" :to="item.path" class="nav-link" :class="{ current: route.path === item.path || (item.path !== '/' && route.path.startsWith(`${item.path}/`)) || (item.path === '/learn' && route.path.startsWith('/lesson/')) }"><component :is="item.icon" :size="18" aria-hidden="true" /> {{ item.text }}</RouterLink>
        </div>
      </nav>
      <div class="sidebar-status"><span class="dot" /><span><strong>{{ showcase ? 'Read-only showcase' : 'Local workspace' }}</strong><small>{{ showcase ? 'Prerecorded samples' : 'Loopback access' }}</small></span></div>
    </aside>
    <div class="workspace">
      <header class="topbar">
        <div class="breadcrumbs"><button class="icon-button menu-toggle" :aria-expanded="menu" aria-controls="workspace-navigation" :aria-label="menu ? 'Close navigation' : 'Open navigation'" @click="menu = !menu"><X v-if="menu" :size="20" aria-hidden="true" /><Menu v-else :size="20" aria-hidden="true" /></button><span class="breadcrumb-root">Workspace</span><ChevronRight :size="14" class="breadcrumb-root" aria-hidden="true" /><span>{{ pageName }}</span></div>
        <div class="top-actions"><span class="status-pill"><span class="dot" /> Synthetic data</span><button class="icon-button" :aria-label="theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'" @click="setTheme(theme === 'dark' ? 'light' : 'dark')"><Sun v-if="theme === 'dark'" :size="19" aria-hidden="true" /><Moon v-else :size="19" aria-hidden="true" /></button></div>
      </header>
      <main id="main-content" ref="main" tabindex="-1" class="content">
        <div v-if="loadError" class="error-box" role="alert"><p>{{ loadError }}</p><button class="button secondary" @click="refresh">Retry loading</button></div>
        <p v-if="loading && route.path !== '/'" class="muted" role="status">Loading lab data…</p>
        <RouterView />
      </main>
      <footer class="workspace-footer"><span>ThreatHuntX Community Lab</span><RouterLink to="/about">Open-source project</RouterLink></footer>
    </div>
  </div>
</template>
