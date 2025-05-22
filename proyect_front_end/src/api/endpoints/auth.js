import api from "../axios";

export default {

    login(credentials) {
        return api.post('/login', credentials);
    },

    register(credentials) {
        return api.post('/registrar', credentials);
    }
}