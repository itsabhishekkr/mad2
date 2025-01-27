import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import ServiceManagement from './components/ServiceManagement.vue';
import AdminUpdateServices from './components/AdminUpdateServices.vue';


const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: LoginPage },
  { path: '/admin/dashboard', component: AdminDashboard },
  {path: '/admin/services', component: ServiceManagement},
  {
    path: '/admin/service/update/:id',
    component: AdminUpdateServices,
    name: 'AdminUpdateService', // Add a name to make navigation easier
    props: true, // Pass `id` as a prop to the component
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;