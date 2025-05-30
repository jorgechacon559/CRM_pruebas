<script setup>
import { reactive, onMounted, ref, watch } from 'vue';
import { useVentasStore } from '@/stores/ventas';
import { useUsuariosStore } from '@/stores/usuarios';
import { useProductsStore } from '@/stores/products';
import ModalGenVenta from './ModalGenVenta.vue';
import Toast from '@/components/Toast.vue'

const headers = reactive(['fecha', 'Cantidad de artículos', 'total']);

const ventas = useVentasStore();
const usuarios = useUsuariosStore();
const productos = useProductsStore();

const showToast = ref(false)
const toastMsg = ref('')
const toastType = ref('success')

const modalGenFather = ref(null);
const pageInput = ref('');

// Sincroniza el input con la página actual
watch(() => ventas.currentPage, (val) => {
  pageInput.value = val;
});

const goToPage = async (page) => {
    if (page < 1 || page > ventas.totalPages) return;
    await ventas.getAllInfoVnt('ventas', page);
};

const openModal = () => {
    modalGenFather.value.openModal();
};

const getInfo = async () => {
    await ventas.getAllInfoVnt('ventas', ventas.currentPage || 1);
    await usuarios.getAllInfoUsr('usuarios');
    await productos.getAllInfoPrd('productos');
};

const toAdded = (item) => {
    ventas.setAdded(item)
    openModal();
};

const deleteItem = async (id) => {
    try {
        const response = await ventas.deleteItemVnt({ 'option': 'ventas', id })
        if (!response.success) throw { message: 'Error al eliminar producto' };
        // Si la página queda vacía tras eliminar, ve a la anterior
        if (ventas.data.length === 1 && ventas.currentPage > 1) {
            await goToPage(ventas.currentPage - 1);
        } else {
            await goToPage(ventas.currentPage);
        }
    } catch (error) {
        console.log(error.message)
    }
};

onMounted(async () => {
    await getInfo();
});

function mostrarToast(msg, tipo = 'success') {
  toastMsg.value = msg
  toastType.value = tipo
  showToast.value = true
  setTimeout(() => showToast.value = false, 2500)
}
</script>

<template>
    <div class="container-all-sails">
        <Toast :show="showToast" :message="toastMsg" :type="toastType" />
        <ModalGenVenta
            ref="modalGenFather"
            @allFine="(msg) => { getInfo(); mostrarToast(msg, 'success'); }"
        />
        <h2>Todos las ventas:</h2>
        <button @click="openModal">Crear venta</button>
        <div class="table">
            <div class="table-heads">
                <div v-for="(head, index) in headers" :key="index" :class="{ 'centered': index > 0 }">
                    <p>{{ head }}</p>
                </div>
            </div>
            <div class="table-data">
                <div class="table-row" v-for="(item, index) in ventas.data" :key="item.venta_id">
                    <div>
                        <p>{{ item.fecha }}</p>
                    </div>
                    <div class="centered">
                        <p>{{ item.cantidad_art }}</p>
                    </div>
                    <div class="centered">
                        <p>${{ Number(item.total).toFixed(2) }}</p>
                    </div>
                    <button class="btn-delete" @click="deleteItem(item.venta_id)">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="5" x2="15" y2="15"/>
                            <line x1="15" y1="5" x2="5" y2="15"/>
                        </svg>
                    </button>
                </div>
            </div>

            <div class="paginator">
                <div class="paginator-controls">
                    <button @click="goToPage(ventas.currentPage - 1)" :disabled="ventas.currentPage <= 1">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                            <path d="M12 2a10 10 0 0 1 .324 19.995l-.324 .005l-.324 -.005a10 10 0 0 1 .324 -19.995zm.707 5.293a1 1 0 0 0 -1.414 0l-4 4a1.048 1.048 0 0 0 -.083 .094l-.064 .092l-.052 .098l-.044 .11l-.03 .112l-.017 .126l-.003 .075l.004 .09l.007 .058l.025 .118l.035 .105l.054 .113l.043 .07l.071 .095l.054 .058l4 4l.094 .083a1 1 0 0 0 1.32 -1.497l-2.292 -2.293h5.585l.117 -.007a1 1 0 0 0 -.117 -1.993h-5.586l2.293 -2.293l.083 -.094a1 1 0 0 0 -.083 -1.32z"></path>
                        </svg>
                    </button>

                    <p>
                        {{ ventas.currentPage }} / {{ ventas.totalPages }}
                    </p>
                    <button @click="goToPage(ventas.currentPage + 1)" :disabled="ventas.currentPage >= ventas.totalPages">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24">
                            <path d="M12 2l.324 .005a10 10 0 1 1 -.648 0l.324 -.005zm.613 5.21a1 1 0 0 0 -1.32 1.497l2.291 2.293h-5.584l-.117 .007a1 1 0 0 0 .117 1.993h5.584l-2.291 2.293l-.083 .094a1 1 0 0 0 1.497 1.32l4 -4l.073 -.082l.064 -.089l.062 -.113l.044 -.11l.03 -.112l.017 -.126l.003 -.075l-.007 -.118l-.029 -.148l-.035 -.105l-.054 -.113l-.071 -.111a1.008 1.008 0 0 0 -.097 -.112l-4 -4z"></path>
                        </svg>
                    </button>
                </div>

                <input
                    type="number"
                    :min="1"
                    :max="ventas.totalPages"
                    placeholder="Ir a página..."
                    v-model.number="pageInput"
                    @keyup.enter="goToPage(pageInput)"
                    @blur="goToPage(pageInput)"
                >
                <br>
            </div>
        </div>
    </div>
</template>
<style scoped lang="scss">
.table {
    display: grid;
    width: 100%;
    gap: .125rem;

    &-heads {
        display: grid;
        text-transform: capitalize;
        grid-template-columns: 2fr 1fr 1fr 0.7fr;
        gap: .125rem;
    }

    &-data {
        display: grid;
        gap: .125rem;
    }

    &-row {
        display: grid;
        grid-template-columns: 2fr 1fr 1fr 0.7fr;
        gap: .125rem;

        >div {
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 1;
            line-clamp: 1;
            overflow: hidden;
        }

        button {
            display: grid;
            place-items: center;
        }
    }
}

.paginator {
    display: flex;
    align-items: center;
    justify-content: space-between;

    &-controls {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0 .5rem;
    }

    input {
        width: 6.375rem;
    }

    button {
        padding: 0;
        display: grid;
        place-items: center;
        background-color: rgb(142, 183, 222);
        border: none;
    }
}

.centered {
    text-align: center;
}

.btn-delete {
  background: #fff;
  border: 1.5px solid #e5e7eb;
  color: #e53e3e;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  transition: background 0.2s, border 0.2s, color 0.2s;
  box-shadow: 0 1px 4px rgba(229,62,62,0.04);
  font-size: 1.3rem;
}

.btn-delete:hover {
  background: #ffeaea;
  border-color: #e53e3e;
  color: #b91c1c;
}
</style>