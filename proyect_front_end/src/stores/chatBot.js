import { defineStore } from "pinia";
import general from "@/api/endpoints/general";

export const useChatbotStore = defineStore('chatbot', () => {
    const addItemBot = async (item) => {
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

    return { addItemBot }
})

