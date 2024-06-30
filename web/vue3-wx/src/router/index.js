import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/login'
    },
    {
      path: '/login',
      component: () => import('@/views/login/LoginPage.vue')
    },
    // 切割试卷界面
    {
      path: '/carve',
      component: () => import('@/views/test/CarvePage.vue')
    },
    // 阅卷任务分配界面
    {
      path: '/assign',
      component: () => import('@/views/read/ReadAssign.vue')
    },
    // 阅卷具体界面
    {
      path: '/readshow',
      component: () => import('@/views/read/ReadShow.vue')
    },
    {
      path: '/layout',
      redirect: '/home',
      component: () => import('@/views/layout/LayoutPage.vue'),
      children: [
        // home
        {
          path: '/home',
          component: () => import('@/views/layout/HomePage.vue')
        },
        // user
        {
          path: '/user',
          component: () => import('@/views/user/UserPage.vue'),
        },
        // test
        {
          path: '/test',
          component: () => import('@/views/test/TestPage.vue'),
          redirect: '/add',
          children: [
            { path: '/add', component: () => import('@/views/test/AddTest.vue') },
            { path: '/aw', component: () => import('@/views/test/AwPage.vue') }
          ]
        },
        // fenxi
        {
          path: '/fenxi',
          component: () => import('@/views/fenxi/FenxiPage.vue')
        },
        // read
        {
          path: '/read',
          component: () => import('@/views/read/ReadPage.vue')
        }
      ]
    }
  ]
})

export default router
