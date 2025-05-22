import { defineStore } from "pinia";
import general from "@/api/endpoints/general";
import { reactive, toRefs } from "vue";
export const useUsuariosStore = defineStore('usuarios', () => {
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

    const getAllInfoUsr = async (item) => {
        try {
            const response = await general.getAllInfo(item);
            if (!response.data.success) throw response;
            setData(response.data.data);
            return response.data.data;

        } catch (error) {
            return {
                success: false,
                message: error?.message || 'Error al obtener los datos',
                status: error?.status || 500,
            }
        }
    }

    const getInfoByIdUsr = async (item) => {
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

    const addItemUsr = async (item) => {
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

    const editItemUsr = async (item) => {
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

    const deleteItemUsr = async (item) => {
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

    return { ...toRefs(state), setData, setAdded, getAllInfoUsr, getInfoByIdUsr, addItemUsr, editItemUsr, deleteItemUsr }
})

