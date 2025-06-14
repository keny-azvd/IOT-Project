import path from 'path';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import jsconfigPaths from 'vite-jsconfig-paths';

// ----------------------------------------------------------------------

export default defineConfig({
  plugins: [react(), jsconfigPaths()],
  base: '/free', // Caminho base para a aplicação
  define: {
    global: 'window'
  },
  resolve: {
    alias: [
      {
        find: /^~(.+)/,
        replacement: path.join(process.cwd(), 'node_modules/$1')
      },
      {
        find: /^src(.+)/,
        replacement: path.join(process.cwd(), 'src/$1')
      }
    ]
  },
  server: {
    host: true,  // Garante a exposição externa
    port: 5082,  // Porta correta
    open: false, // Evita abrir localmente
    historyApiFallback: true,
  },
  preview: {
    host: true,  // Garante que o preview também seja acessível
    port: 5082,
    historyApiFallback: true,
  }
});
