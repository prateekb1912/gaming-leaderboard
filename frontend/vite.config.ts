import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig(() => {
  return {
    plugins: [react()],
    server: {
      proxy: {
        "/api": "https://gaming-leaderboard-9euy.onrender.com",
      },
    },
  };
});
