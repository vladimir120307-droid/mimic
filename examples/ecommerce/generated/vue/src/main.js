import { createApp } from 'vue';
import { createRouter, createWebHashHistory } from 'vue-router';
import App from './App.vue';
import './index.css';

const routes = [
  { path: "/", component: () => import("./views/Catalog.vue") },
  { path: "/product_detail", component: () => import("./views/Product.vue") },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

createApp(App).use(router).mount('#app');
