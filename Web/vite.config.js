import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import { viteMockServe } from 'vite-plugin-mock';
import { resolve } from 'node:path';

// const target = 'http://localhost:5793/mock/api';
const target = 'http://10.101.14.36:48001/api/';

const root = process.cwd();

export default defineConfig({
  plugins: [vue(), viteMockServe({ mockPath: './mock/', supportTs: false })], //
  resolve: {
    alias: {
      '@': `${resolve(root, 'src')}`,
    },
  },
  server: {
    open: true,
    port: 5793,
    proxy: {
      '/api': {
        target: target,
        secure: false,
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
});
