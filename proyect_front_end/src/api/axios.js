import axios from "axios";
import { useAuthStore } from "@/stores/auth";

const api = axios.create({
  baseURL: "http://127.0.0.1:5000/api",
  headers: {
    "Content-Type": "application/json",
  },
});

// Interceptor para añadir token de autenticación desde sessionStorage
api.interceptors.request.use((config) => {
  const token = sessionStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores de autenticación (401) y refrescar token
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response && error.response.status === 401) {
      const refreshToken = sessionStorage.getItem("refresh_token");
      // Solo intenta refrescar si hay refresh_token y no es un intento de refresh
      if (refreshToken && !error.config._retry && !error.config.url.endsWith('/refresh')) {
        error.config._retry = true;
        try {
          // Usamos el store de auth para refrescar el token
          const authStore = useAuthStore();
          const refreshed = await authStore.refreshAccessToken();
          if (refreshed) {
            // Reintenta la petición original con el nuevo token
            error.config.headers.Authorization = `Bearer ${sessionStorage.getItem("token")}`;
            return api.request(error.config);
          }
        } catch (e) {
          // Si falla el refresh, sigue con logout abajo
        }
      }
      // Si no hay refresh_token o falla el refresh, cerrar sesión
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("refresh_token");
      sessionStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;