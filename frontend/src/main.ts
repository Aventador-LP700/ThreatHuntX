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
  ['simulate', 'Guided Hunt'], ['alerts', 'Alerts'], ['hunt', 'Investigation Workspace'], ['matrix', 'MITRE Matrix'],
  ['investigations', 'Recent Investigations'], ['rules', 'Detection Studio'], ['playbooks', 'Playbooks'],
  ['progress', 'Reports'], ['architecture', 'Reference Architecture'], ['deployment', 'Deployment Help'], ['about', 'Community'],
].map(([page, title]) => ({ path: `/${page}`, component: Workspace, props: { page }, meta: { title } }))
const router = createRouter({
  history: createWebHashHistory(),
  scrollBehavior: (_to, _from, saved) => saved ?? { top: 0 },
  routes: [
    { path: '/', component: Home, meta: { title: 'Home' } },
    { path: '/learn', component: Explorer, props: { learning: true }, meta: { title: 'Learning Paths' } },
    { path: '/techniques', component: Explorer, props: { learning: false }, meta: { title: 'Technique Map' } },
    { path: '/lesson/:id', component: Lesson, props: true, meta: { title: 'Guided Lesson' } },
    { path: '/investigations/:id/report', component: Investigation, props: route => ({ id: String(route.params.id), printable: true }), meta: { title: 'Case Report' } },
    { path: '/investigations/:id', component: Investigation, props: true, meta: { title: 'Evidence Timeline' } },
    { path: '/rules/:id', component: Workspace, props: route => ({ page: 'rules', id: String(route.params.id) }), meta: { title: 'Detection Rule' } },
    ...workspace,
    { path: '/:pathMatch(.*)*', redirect: '/' },
  ],
})

createApp(App).use(router).mount('#app')
