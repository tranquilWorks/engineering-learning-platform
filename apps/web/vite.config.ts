import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/api": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
  build: {
    sourcemap: true,
    chunkSizeWarningLimit: 1800,
    rollupOptions: {
      output: {
        manualChunks: {
          plotly: ["plotly.js-dist-min"],
          markdown: ["react-markdown", "remark-gfm", "remark-math", "rehype-katex", "katex"],
        },
      },
    },
  },
});
