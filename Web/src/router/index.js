import { createRouter, createWebHistory } from 'vue-router';
import images from './modules/images';
import home from './modules/home';

const routerHistory = createWebHistory();

const routes = [
  {
    path: '/',
    name: 'App',
    children: [...images, ...home],
  },
];

const router = createRouter({
  history: routerHistory,
  routes,
  scrollBehavior(to, from, savedPosition) {
    // always scroll to top
    return { top: 0 };
  },
});

export default router;
