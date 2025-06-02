import auth from "@/api/endpoints/auth";
import router from "@/router";
import { defineStore } from "pinia";
import api from "@/api/axios";

export const useAuthStore = defineStore("auth", {
    state: () => ({
        user: null,
        token: null,
        refreshToken: null,
        isAuthenticated: false,
    }),
    actions: {
        async login(email, password) {
            try {
                const credentials = { email, password };
                const response = await auth.login(credentials);
                if (!response.data.access_token) {
                    throw new Error("Credenciales incorrectas");
                }
                this.user = {
                    usuario_id: response.data.usuario_id,
                    nombre: response.data.nombre,
                    apellido: response.data.apellido,
                    rol: response.data.rol,
                    email: response.data.email
                };
                this.token = response.data.access_token;
                this.refreshToken = response.data.refresh_token;
                this.isAuthenticated = true;
                sessionStorage.setItem("user", JSON.stringify(this.user));
                sessionStorage.setItem("token", this.token);
                sessionStorage.setItem("refresh_token", this.refreshToken);
                router.push("/inicio");
            } catch (error) {
                console.error(error);
                throw error;
            }
        },

        setUser(payload) {
            this.user = payload;
            sessionStorage.setItem("user", JSON.stringify(payload));
        },

        async logout() {
            try {
            } catch (error) {
                console.error(error);
            } finally {
                sessionStorage.removeItem("token");
                sessionStorage.removeItem("refresh_token");
                sessionStorage.removeItem("user");
                this.user = null;
                this.token = null;
                this.refreshToken = null;
                this.isAuthenticated = false;
                router.push("/login");
            }
        },

        async register(name, apellido, correo, password) {
            try {
                const credentials = {
                    nombre: name,
                    apellido: apellido,
                    email: correo,
                    password: password,
                };
                const response = await auth.register(credentials);
                return response;
            } catch (error) {
                throw error;
            }
        },

        async refreshAccessToken() {
            try {
                const refresh_token = sessionStorage.getItem("refresh_token");
                if (!refresh_token) throw new Error("No refresh token");
                const response = await api.post("/refresh", {}, {
                    headers: { Authorization: `Bearer ${refresh_token}` }
                });
                this.token = response.data.access_token;
                sessionStorage.setItem("token", this.token);
                return true;
            } catch (error) {
                await this.logout();
                return false;
            }
        },

        initialize() {
            const token = sessionStorage.getItem("token");
            const refreshToken = sessionStorage.getItem("refresh_token");
            const user = sessionStorage.getItem("user");
            if (token && refreshToken && user) {
                this.token = token;
                this.refreshToken = refreshToken;
                this.user = JSON.parse(user);
                this.isAuthenticated = true;
            }
        }
    },
});