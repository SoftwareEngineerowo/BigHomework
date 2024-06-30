import { fileURLToPath, URL } from 'node:url'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver} from 'unplugin-vue-components/resolvers'
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

import externalGlobals from 'rollup-plugin-external-globals';
import { visualizer } from 'rollup-plugin-visualizer'
import { ViteImageOptimizer } from 'vite-plugin-image-optimizer';
import viteCompression from 'vite-plugin-compression'

const globals = externalGlobals({
  moment: 'moment',
  'video.js': 'videojs',
  jspdf: 'jspdf',
  xlsx: 'XLSX',
});

export default defineConfig({
  build: {
    rollupOptions: {
      external: ['moment', 'video.js', 'jspdf', 'xlsx'],
      plugins: [globals],
    },
    minify: 'terser',
    // 清除所有console和debugger
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true
      }
    }
  },
  plugins: [
    vue(),
    // 自动导入
    AutoImport({
      resolvers: [
        ElementPlusResolver(),
          // 自动导入图标组件
          // IconsResolver({
          //   prefix: 'Icon',
          // }),
  
      ]
    }),
    // 自动注册
    Components({
      resolvers: [
        ElementPlusResolver(),
         // 自动注册图标组件
        //  IconsResolver({
        //   enabledCollections: ['ep'],
        // })
      ]
    }),
    // 打包分析工具
    visualizer(),
    // 图片压缩
    ViteImageOptimizer(),
    // gzip代码压缩
    viteCompression()

  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  }
})
