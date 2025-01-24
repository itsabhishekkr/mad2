// filepath: /home/abhishek/householdservices/frontend/src/routes.js
import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import CustomerSignUp from './components/CustomerSignUp.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/signup', component: CustomerSignUp }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;