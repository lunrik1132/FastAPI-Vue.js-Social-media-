import { useUserStore } from '@/stores/user'
import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'index'
        },
        {
            path: '/user/:id',
            component: () => import('@/pages/users/UserPage.vue'),
            name: 'users.index'
        },
        {
            path: '/user/:id/friends',
            component: () => import('@/pages/users/UserFriendsPage.vue'),
            name: 'users.friends.index'
        },
        {
            path: '/login',
            component: () => import('@/pages/users/LoginPage.vue'),
            name: 'login.index'
        },
        {
            path: '/register',
            component: () => import('@/pages/users/RegisterPage.vue'),
            name: 'register.index'
        },
        {
            path: '/settings',
            component: () => import('@/pages/users/SettingsPage.vue'),
            name: 'settings.index',
            meta: { requiresAuth: true }
        },
        {
            path: '/feed',
            component: () => import('@/pages/FeedPage.vue'),
            name: 'feed.index'
        },
        {
            path: '/friends',
            component: () => import('@/pages/FriendsPage.vue'),
            name: 'friends.index',
            meta: { requiresAuth: true }
        },
        {
            path: '/messages/:id',
            component: () => import('@/pages/ChatPage.vue'),
            name: 'messages.chat.index',
            meta: { requiresAuth: true }
        },
        {
            path: '/messages',
            component: () => import('@/pages/MessagesPage.vue'),
            name: 'messages.index',
            meta: { requiresAuth: true }
        },
        {
            path: '/chat',
            component: () => import('@/pages/ChatPage.vue'),
            name: 'chat.index'
        },
    ],
    scrollBehavior(to, from, savedPosition) {
        if (savedPosition) {
            return savedPosition
        }

        return { top: 0 }
    }
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()

    if (to.name === "index")
    {
        next({ name: "feed.index" })
    }

  if (to.meta.requiresAuth && !userStore.isAuth) {
    next({ name: "login.index" })
  } else {
    next()
  }
})


export default router
