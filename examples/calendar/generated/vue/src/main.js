import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import './index.css';

const routes = [
  { path: "/", component: () => import("./views/Month.vue") },
  { path: "/event_detail", component: () => import("./views/EventDetail.vue") },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
