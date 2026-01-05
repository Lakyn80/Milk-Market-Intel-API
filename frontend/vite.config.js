import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  server: {
    fs: {
      // allow reading analytics files from the backend folder
      allow: [resolve(__dirname, "..")],
    },
  },
});
