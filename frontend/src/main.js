import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router/router'

const app = createApp(App)
const pinia = createPinia()

app.provide('apiUrl', 'https://fastapi-vue-js-social-media-1.onrender.com')

app.use(router)
   .use(pinia)

app.mount('#app')
