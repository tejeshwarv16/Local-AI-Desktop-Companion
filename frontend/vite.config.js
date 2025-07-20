// vite.config.js
import { defineConfig } from 'vite'
import electron from 'vite-plugin-electron'
import renderer from 'vite-plugin-electron-renderer'

export default defineConfig({
  plugins: [
    electron([
      {
        // Main process entry file
        entry: 'main.js',
      },
    ]),
    renderer(),
  ],
})