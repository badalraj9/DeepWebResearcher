import path from "path"
import react from "@vitejs/plugin-react"
import { defineConfig } from "vite"
import viteCompression from 'vite-plugin-compression';
import { visualizer } from 'rollup-plugin-visualizer';

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    viteCompression(), // Default is gzip
    viteCompression({ algorithm: 'brotliCompress', ext: '.br' }), // Add Brotli
    visualizer({
      open: false,
      gzipSize: true,
      brotliSize: true,
    })
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    target: 'esnext', // Use modern JS
    minify: 'esbuild', // Faster minification
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom', 'framer-motion'],
          ui: ['@radix-ui/react-alert-dialog', '@radix-ui/react-dialog', '@radix-ui/react-slot', '@radix-ui/react-toast', 'lucide-react', 'sonner'],
          editor: [
             '@tiptap/react',
             '@tiptap/starter-kit',
             '@tiptap/extension-bubble-menu',
             '@tiptap/extension-image',
             '@tiptap/extension-link',
             '@tiptap/extension-placeholder'
          ]
        }
      }
    }
  }
})
