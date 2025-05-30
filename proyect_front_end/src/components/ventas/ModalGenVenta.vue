<script setup>
import { ref, defineExpose, reactive, computed, watch, onMounted } from 'vue';
import { useVentasStore } from '@/stores/ventas';
import { useProductsStore } from '@/stores/products';

const ModalGenVenta = ref(null);
const emit = defineEmits(['allFine']);

const buscadorPrd = ref(null);
const userSelected = ref({
    nombre: null,
    apellido: null,
    email: null,
    usuario_id: null
});

const ventas = useVentasStore();
const ventasAdded = computed(() => ventas.added);

const products = useProductsStore();
const productsData = computed(() => {
    const searchValuePrd = buscadorPrd.value?.toLowerCase().trim();
    if (!searchValuePrd) return [];
    return products.data.filter(item =>
        item.nombre?.toLowerCase().includes(searchValuePrd)
    ).slice(0, 5);
});

const addProduct = (product) => {
    const existingProduct = dataToSend.productos.find(
        p => p.producto_id === product.producto_id
    );
    if (!existingProduct) {
        dataToSend.productos.push({ ...product, cantidad: 1 });
    }
    buscadorPrd.value = '';
};

const dataToSend = reactive({
    venta_id: null,
    usuario_id: null,
    fecha: null,
    total: null,
    cantidad_art: null,
    productos: [],
});

const deleteOnProduct = (index) => dataToSend.productos.splice(index, 1);

const identity = ref(null);
onMounted(() => {
    const user = sessionStorage.getItem('user');
    identity.value = user ? JSON.parse(user) : null;
});

watch(ventasAdded, (newVenta) => {
    if (newVenta) {
        Object.assign(userSelected.value, identity.value || {});
        dataToSend.venta_id = newVenta.venta_id;
        dataToSend.usuario_id = newVenta.usuario_id;
        dataToSend.fecha = newVenta.fecha;
        dataToSend.total = newVenta.total;
        dataToSend.cantidad_art = newVenta.cantidad_art;
        dataToSend.productos = newVenta.productos ? [...newVenta.productos] : [];
    } else {
        resetForm();
    }
});

watch(
    () => dataToSend.productos,
    () => {
        dataToSend.total = dataToSend.productos.reduce(
            (acc, producto) => acc + producto.precio * producto.cantidad,
            0
        );
        dataToSend.cantidad_art = dataToSend.productos.reduce(
            (acc, producto) => acc + producto.cantidad,
            0
        );
    },
    { deep: true }
);

const openModal = () => {
    if (identity.value) {
        dataToSend.usuario_id = identity.value.usuario_id;
        Object.assign(userSelected.value, identity.value);
    }
    ModalGenVenta.value.showModal();
    requestAnimationFrame(() => {
        window.addEventListener('click', clickOutside);
        window.addEventListener('keydown', handleEsc);
    });
};

const closeModal = () => {
    ModalGenVenta.value?.close();
    window.removeEventListener('click', clickOutside);
    window.removeEventListener('keydown', handleEsc);
    ventas.setAdded(null);
    resetForm();
};

const resetForm = () => {
    Object.assign(userSelected.value, identity.value || {
        nombre: null,
        apellido: null,
        email: null,
        usuario_id: null
    });
    dataToSend.venta_id = null;
    dataToSend.usuario_id = identity.value ? identity.value.usuario_id : null;
    dataToSend.fecha = null;
    dataToSend.total = null;
    dataToSend.cantidad_art = null;
    dataToSend.productos = [];
};

const clickOutside = (e) => {
    if (!ModalGenVenta.value?.open) return;
    const rect = ModalGenVenta.value.getBoundingClientRect();
    const isInDialog =
        e.clientX >= rect.left &&
        e.clientX <= rect.right &&
        e.clientY >= rect.top &&
        e.clientY <= rect.bottom;
    if (!isInDialog) closeModal();
};

const handleEsc = (e) => {
    if (e.key === "Escape") closeModal();
};

const submitData = async () => {
    if (!dataToSend.usuario_id) {
        alert('No se detectó usuario autenticado');
        return;
    }
    if (!dataToSend.productos.length) {
        alert('Agrega al menos un producto');
        return;
    }
    if (dataToSend.productos.some(p => p.cantidad < 1 || p.cantidad > p.stock)) {
        alert('Verifica las cantidades de los productos');
        return;
    }

    try {
        const item = { ...dataToSend };
        const ruta = item.venta_id ? 'editItemVnt' : 'addItemVnt';
        const option = item.venta_id ? `ventas/${item.venta_id}` : 'ventas'
        const response = await ventas[ruta]({ option, item });

        if (response.success) {
            emit('allFine', '¡Venta registrada correctamente!');
            closeModal();
        } else {
            throw new Error('Ha ocurrido un error');
        }
    } catch (error) {
        console.error(error.message);
    }
};

defineExpose({
    openModal,
});
</script>

<template>
    <dialog ref="ModalGenVenta" class="modal-gen-venta">
        <form class="container-modal" @submit.prevent="submitData">
            <h2 class="modal-title">{{ dataToSend.venta_id ? 'Editar venta' : 'Nueva venta' }}</h2>
            <div class="form-group">
                <label>Usuario</label>
                <div class="selected-user">
                    <span v-if="userSelected.nombre">{{ userSelected.nombre }} {{ userSelected.apellido }}</span>
                    <span v-else class="no-user">Ninguno</span>
                </div>
            </div>

            <div class="form-group">
                <label for="fecha">Fecha</label>
                <input type="date" id="fecha" v-model="dataToSend.fecha" class="form-control">
            </div>

            <div class="form-group">
                <label for="searcherPrd">Buscador de productos</label>
                <input type="text" v-model="buscadorPrd" id="searcherPrd" class="form-control"
                    placeholder="Buscar producto por nombre">
                <div class="height-ancor" v-if="buscadorPrd && buscadorPrd.length > 0">
                    <div class="button-list">
                        <button v-for="(item, index) in productsData" :key="index" type="button" @click="addProduct(item)">
                            {{ item.nombre }}
                        </button>
                    </div>
                </div>
            </div>

            <div class="form-group" v-for="(item, index) in dataToSend.productos" :key="index">
                <div class="productWrapper">
                    <div class="product-info">
                        <p><b>{{ item.nombre }}</b> <span style="color: #888;">(Stock: {{ item.stock }})</span></p>
                        <p>Precio: ${{ item.precio }}</p>
                    </div>
                    <div class="product-actions">
                        <input
                            type="number"
                            class="form-control"
                            placeholder="Cantidad"
                            v-model.number="item.cantidad"
                            :min="1"
                            :max="item.stock"
                            @input="item.cantidad = Math.max(1, Math.min(item.cantidad, item.stock))"
                        >
                        <span class="subtotal" v-if="item.cantidad > 0">
                            Subtotal: ${{ (item.cantidad * Number(item.precio)).toFixed(2) }}
                        </span>
                        <button type="button" class="btn-delete" @click="deleteOnProduct(index)">
                            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                                stroke-linecap="round" stroke-linejoin="round" width="20" height="20" stroke-width="2">
                                <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0-18 0"></path>
                                <path d="M9 12l6 0"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>

            <div class="form-group">
                <label for="total">Total</label>
                <input type="number" id="total" :value="Number(dataToSend.total).toFixed(2)" class="form-control" disabled>
            </div>

            <div class="form-group">
                <label for="cantidad_art">Cantidad de artículos</label>
                <input type="number" id="cantidad_art" v-model="dataToSend.cantidad_art" class="form-control" disabled>
            </div>

            <div class="modal-actions">
                <button type="submit" class="btn-primary" :disabled="!dataToSend.usuario_id || !dataToSend.productos.length">Guardar</button>
                <button type="button" class="btn-secondary" @click="closeModal">Cancelar</button>
            </div>
        </form>
    </dialog>
</template>

<style scoped lang="scss">
.modal-gen-venta {
    border: none;
    padding: 0;
    background: transparent;
}

.container-modal {
    background: #fff;
    border-radius: 1.5rem;
    box-shadow: 0 8px 32px rgba(37,99,235,0.12);
    padding: 2.5rem 2.5rem 2rem 2.5rem;
    min-width: 340px;
    max-width: 95vw;
    width: 400px;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
}

.modal-title {
    text-align: center;
    color: #2563eb;
    font-weight: 700;
    font-size: 2rem;
    margin-bottom: 0.5rem;
    letter-spacing: -1px;
}

.form-group {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

label {
    color: #2563eb;
    font-weight: 600;
    font-size: 1rem;
}

.form-control {
    width: 100%;
    box-sizing: border-box;
    padding: 0.9rem 1rem;
    border: 1.5px solid #e5e7eb;
    border-radius: 0.7rem;
    font-size: 1rem;
    background-color: #f7f8fa;
    color: #222;
    transition: border 0.2s;
    resize: none;
}

.form-control:focus {
    border-color: #2563eb;
    outline: none;
    background: #fff;
}

.selected-user {
    padding: 0.5rem 1rem;
    background: #f1f5ff;
    border-radius: 0.7rem;
    color: #2563eb;
    font-weight: 600;
}

.no-user {
    color: #888;
    font-style: italic;
}

.height-ancor {
    min-height: 1.5rem;
    z-index: 3;
}

.button-list {
    display: grid;
    grid-template-rows: 0fr;
    overflow: hidden;
    transition: grid-template-rows 0.3s ease;
    height: fit-content;
}

.button-list div {
    display: grid;
    gap: 0.5rem;
    padding-top: 0.5rem;
    background-color: #f7f8fa;
    border-radius: 0.7rem;
}

.button-list.active {
    grid-template-rows: 1fr;
}

.button-list button {
    padding: 0.5rem 1rem;
    background-color: #e5e7eb;
    border: none;
    border-radius: 0.4rem;
    text-align: left;
    font-size: 0.95rem;
    cursor: pointer;
    color: #2563eb;
    font-weight: 600;
    transition: background-color 0.2s;
}

.button-list button:hover {
    background-color: #c7d7fa;
}

.productWrapper {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    background: #f7f8fa;
    border-radius: 0.7rem;
    padding: 0.7rem 1rem;
    margin-bottom: 0.5rem;
    position: relative;
}

.product-info {
    display: flex;
    flex-direction: column;
    gap: 0.2rem;
}

.product-actions {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.subtotal {
    color: #2563eb;
    font-weight: 600;
}

.btn-delete {
    background: #fff;
    border: 1.5px solid #e5e7eb;
    color: #e53e3e;
    border-radius: 50%;
    width: 2.2rem;
    height: 2.2rem;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 0;
    transition: background 0.2s, border 0.2s, color 0.2s;
    box-shadow: 0 1px 4px rgba(229,62,62,0.04);
    font-size: 1.1rem;
}

.btn-delete:hover {
    background: #ffeaea;
    border-color: #e53e3e;
    color: #b91c1c;
}

.modal-actions {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 0.5rem;
}

.btn-primary {
    background-color: #2563eb;
    color: #fff;
    padding: 0.9rem 1.5rem;
    border: none;
    border-radius: 0.7rem;
    cursor: pointer;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 2px 8px rgba(37,99,235,0.10);
    transition: background 0.2s;
}

.btn-primary:disabled {
    background: #b6d0fa;
    cursor: not-allowed;
}

.btn-primary:hover:not(:disabled) {
    background-color: #1e40af;
}

.btn-secondary {
    background: #fff;
    color: #2563eb;
    border: 1.5px solid #2563eb;
    border-radius: 0.7rem;
    padding: 0.9rem 1.5rem;
    font-weight: 700;
    font-size: 1.1rem;
    cursor: pointer;
    transition: background 0.2s, color 0.2s, border 0.2s;
}

.btn-secondary:hover {
    background: #2563eb;
    color: #fff;
}
</style>