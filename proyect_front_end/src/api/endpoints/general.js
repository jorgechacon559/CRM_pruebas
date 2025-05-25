import api from "../axios";

export default {
    getAllInfo(payload, page = 1) {
        return api.get(`/${payload}?page=${page}`);
    },

    getInfoById(payload) {
        return api.get(`/${payload.option}/${payload.id}`);
    },

    deleteItem(payload) {
        return api.delete(`/${payload.option}/${payload.id}`);
    },

    addItem(payload) {
        return api.post(`/${payload.option}`, payload.item);
    },

    editItem(payload) {
        return api.put(`/${payload.option}/${payload.id}`, payload.item);
    },
}