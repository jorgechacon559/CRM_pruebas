import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
  baseURL: "http://localhost:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Añade el token de autenticación a las peticiones, excepto en /refresh
api.interceptors.request.use((config) => {
  if (!config.url.endsWith('/refresh')) {
    const token = sessionStorage.getItem("token");
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
  }
  return config;
});

// Maneja errores 401 intentando refrescar el token una vez
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response && error.response.status === 401) {
      const refreshToken = sessionStorage.getItem("refresh_token");
      if (refreshToken && !error.config._retry && !error.config.url.endsWith('/refresh')) {
        error.config._retry = true;
        try {
          const authStore = useAuthStore();
          const refreshed = await authStore.refreshAccessToken();
          if (refreshed) {
            error.config.headers.Authorization = `Bearer ${sessionStorage.getItem("token")}`;
            return api.request(error.config);
          }
        } catch (e) {
          // Si falla el refresh, se hace logout abajo
        }
      }
      // Elimina credenciales y redirige a login si no es posible refrescar
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("refresh_token");
      sessionStorage.removeItem("user");
      if (
        window.location.pathname !== "/login" &&
        !error.config.url.endsWith('/login')
      ) {
        window.location.href = "/login";
      };
    }
    return Promise.reject(error);
  }
);

export default api;