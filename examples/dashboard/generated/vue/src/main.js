import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import './index.css';

const routes = [
  { path: "/", component: () => import("./views/Home.vue") },
  { path: "/details", component: () => import("./views/Activity.vue") },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
