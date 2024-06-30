import '@/assets/reset.css'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import persist from 'pinia-plugin-persistedstate'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

import {Button,Tour} from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';

const app = createApp(App)
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

app.use(Tour)
app.use(Button)

app.use(createPinia().use(persist))
app.use(router)
app.mount('#app')
