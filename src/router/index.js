import { createRouter, createWebHistory } from 'vue-router';
import Home from '../views/Home.vue';
import Login from '../views/Login.vue';
import Signup from '../views/Signup.vue'; // 회원가입 페이지 추가

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: Signup, // 회원가입 페이지 경로
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
