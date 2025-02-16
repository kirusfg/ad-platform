import { defineConfig } from 'vite'
import { resolve } from 'path'

export default defineConfig({
    root: resolve('./static_src/'),
    base: '/static/',
    build: {
        outDir: resolve('./static'),
        rollupOptions: {
            input: {
                mainEntry: resolve('./static_src/main.js'),
            },
        },
        manifest: "manifest.json",
    },
    plugins: [],
    server: {
        origin: 'http://127.0.0.1:5173',
    },
})