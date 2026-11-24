import { createApp } from 'vue'
import { createRouter, createWebHashHistory } from 'vue-router'
import App from './App.vue'
import Home from './views/Home.vue'
import Lesson from './views/Lesson.vue'
import Investigation from './views/Investigation.vue'
import Explorer from './views/Explorer.vue'
import Workspace from './views/Workspace.vue'
import './styles.css'

const workspace = [
  ['simulate', 'Simulate'], ['alerts', 'Alerts'], ['hunt', 'Hunt Workspace'], ['matrix', 'ATT&CK Matrix'],
  ['investigations', 'Investigations'], ['rules', 'Detection Rules'], ['playbooks', 'Playbooks'],
  ['progress', 'Learning Progress'], ['deployment', 'Deployment Help'], ['about', 'About / Contribute'],
].map(([page, title]) => ({ path: `/${page}`, component: Workspace, props: { page }, meta: { title } }))
const router = createRouter({
  history: createWebHashHistory(),
  scrollBehavior: (_to, _from, saved) => saved ?? { top: 0 },
  routes: [
    { path: '/', component: Home, meta: { title: 'Start Here' } },
    { path: '/learn', component: Explorer, props: { learning: true }, meta: { title: 'Learn' } },
    { path: '/techniques', component: Explorer, props: { learning: false }, meta: { title: 'Technique Explorer' } },
    { path: '/lesson/:id', component: Lesson, props: true, meta: { title: 'Guided Lesson' } },
    { path: '/investigations/:id', component: Investigation, props: true, meta: { title: 'Evidence Timeline' } },
    { path: '/rules/:id', component: Workspace, props: route => ({ page: 'rules', id: String(route.params.id) }), meta: { title: 'Detection Rule' } },
    ...workspace,
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

createApp(App).use(router).mount('#app')
