import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
    root: resolve('./static_src/'),
    base: '/static/',
    build: {
        outDir: resolve('./static/dist'),
        rollupOptions: {
            input: {
                mainEntry: resolve('./static/src/main.js'),
            },
        },
    },
    plugins: [],
    server: {
        origin: 'http://127.0.0.1:5173',
    },
})