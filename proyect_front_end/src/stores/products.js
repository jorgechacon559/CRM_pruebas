import { defineStore } from "pinia";
import general from "@/api/endpoints/general";
import { reactive, toRefs } from "vue";
export const useProductsStore = defineStore('products', () => {
    const state = reactive({
        data: null,
        added: null,
    })

    const setData = (item) => {
        state.data = item
    }

    const setAdded = (item) => {
        state.added = item
    }

    const getAllInfoPrd = async (item) => {
        try {
            const response = await general.getAllInfo(item);
            if (!response.data.productos) throw response;
            setData(response.data.productos);
            return response.data.productos;

        } catch (error) {
            return {
                success: false,
                message: error?.message || 'Error al obtener los datos',
                status: error?.status || 500,
            }
        }
    }

    const getInfoByIdPrd = async (item) => {
        try {
            const response = await general.getInfoById(item);
            if (!response.data) throw response;
            setData(response.data);
            return response.data;

        } catch (error) {
            return {
                success: false,
                message: error.message || 'Error al obtener información específica',
                status: error?.status || 500,
            }
        }
    }

    const addItemPrd = async (item) => {
        try {
            const response = await general.addItem(item);
            if (!response.data) throw response;
            return response.data;

        } catch (error) {
            return {
                success: false,
                message: error.message || 'Error al crear usuario',
                status: error?.status || 500,
            }
        }
    }

    const editItemPrd = async (item) => {
        try {
            const response = await general.editItem(item);
            if (!response.data) throw response;
            return response.data;

        } catch (error) {
            return {
                success: false,
                message: error?.message || 'Error al editar perfil',
                status: error?.status || 500,
            }
        }
    }

    const deleteItemPrd = async (item) => {
        try {
            const response = await general.deleteItem(item);
            if (!response.data) throw response;
            return response.data;

        } catch (error) {
            return {
                success: false,
                message: error?.detail || 'Error al eliminar producto',
                status: error?.status || 500,
            }
        }
    }

    return { ...toRefs(state), setData, setAdded, getAllInfoPrd, getInfoByIdPrd, addItemPrd, editItemPrd, deleteItemPrd }
})

