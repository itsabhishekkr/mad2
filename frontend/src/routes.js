import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './components/HomePage.vue';
import LoginPage from './components/LoginPage.vue';
import AdminDashboard from './components/AdminDashboard.vue';
import ServiceManagement from './components/ServiceManagement.vue';
import AdminUpdateServices from './components/AdminUpdateServices.vue';
import AdminCustomer from './components/AdminCustomer.vue';
import AdminProfessionalDetails from './components/AdminProfessionalDetails.vue';
import CustomerRegister from './components/CustomerRegister.vue';
import ProfessionalRegister from './components/ProfessionalRegister.vue';
import CustomerServiceList from './components/CustomerServiceList.vue';


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
  {path: '/admin/customers', component: AdminCustomer},
  {path: '/admin/professionals', component: AdminProfessionalDetails},
  {path: '/registor/customer', component: CustomerRegister},
  {path: '/registor/professional', component: ProfessionalRegister},
  {path: '/customer/dashboard', component: CustomerServiceList}
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;