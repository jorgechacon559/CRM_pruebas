import api from "../axios";

export default {

    login(credentials) {
        return api.post('/login', credentials);
    },

    logout(credentials) {
        return api.post('/logout');
    },

    register(credentials) {
        return api.post('/registrar', credentials);
    }
}