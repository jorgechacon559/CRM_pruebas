<script setup>
import { ref, defineExpose, reactive, computed, watch } from 'vue';
import { useVentasStore } from '@/stores/ventas';
import { useUsuariosStore } from '@/stores/usuarios';
import { useProductsStore } from '@/stores/products';

const ModalGenVenta = ref(null);

// Emitir eventos
const emit = defineEmits(['allFine']);

const buscador = ref(null);
const buscadorPrd = ref(null);
const userSelected = ref({
    nombre: null,
    apellido: null,
    email: null,
    usuario_id: null
});

// Store y estado reactivo
const ventas = useVentasStore();
const ventasAdded = computed(() => ventas.added);

const usuarios = useUsuariosStore();
const usuariosData = computed(() => usuarios.data);

const products = useProductsStore();
const productsData = computed(() => {
    const searchValuePrd = buscadorPrd.value?.toLowerCase().trim();
    if (!searchValuePrd) return []; const deleteOnProduct = (index) => {
        dataToSend.productos.splice(index, 1);
    }
    // console.log(products.data)

    return products.data.filter(item =>
        item.nombre?.toLowerCase().includes(searchValuePrd)
    ).slice(0, 5);
});

const usuariosDataBuscador = computed(() => {
    const searchValue = buscador.value?.toLowerCase().trim();
    if (!searchValue) return [];

    return usuariosData.value.filter(item =>
        item.nombre?.toLowerCase().includes(searchValue) ||
        item.apellido?.toLowerCase().includes(searchValue) ||
        item.email?.toLowerCase().includes(searchValue)
    ).slice(0, 5);
})

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
    productos: [

    ],
});

const deleteOnProduct = (index) => dataToSend.productos.splice(index, 1);


// Rellenar el formulario automáticamente si hay un producto seleccionado
watch(ventasAdded, (newProduct) => {
    if (newProduct) {
        const selectedUser = usuariosData.value.find(item => item.usuario_id === newProduct.usuario_id);
        Object.assign(userSelected.value, selectedUser || {});
        dataToSend.venta_id = newProduct.venta_id;
        dataToSend.usuario_id = newProduct.usuario_id;
        dataToSend.fecha = newProduct.fecha;
        dataToSend.total = newProduct.total;
        dataToSend.cantidad_art = newProduct.cantidad_art;
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


// Métodos del modal
const openModal = () => {
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

    // Limpiar producto seleccionado en el store y formulario
    ventas.setAdded(null);
    resetForm();
};

// Resetea los datos del formulario
const resetForm = () => {
    buscador.value = null;

    Object.assign(userSelected.value, {
        nombre: null,
        apellido: null,
        email: null,
        usuario_id: null
    });

    dataToSend.venta_id = null;
    dataToSend.usuario_id = null;
    dataToSend.fecha = null;
    dataToSend.total = null;
    dataToSend.cantidad_art = null;
    dataToSend.productos = [];
};

// Detectar clic fuera del modal
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

// Detectar tecla ESC para cerrar el modal
const handleEsc = (e) => {
    if (e.key === "Escape") closeModal();
};

// Enviar datos
const submitData = async () => {
    if (!dataToSend.usuario_id) {
        alert('Selecciona un usuario');
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
            emit('allFine');
            closeModal(); // Cerrar el modal automáticamente si todo está bien
        } else {
            throw new Error('Ha ocurrido un error');
        }
    } catch (error) {
        console.error(error.message);
    }
};

// Exponer métodos al padre
defineExpose({
    openModal,
});

</script>
<!-- UserSearch.vue -->
<template>
    <dialog ref="ModalGenVenta">
        <div class="container-modal">
            <div>
                <label for="searcher">Buscador de usuarios</label>
                <input type="text" v-model="buscador" id="searcher" placeholder="Buscar por nombre, correo o apellido">
                <div class="height-ancor">
                    <div class="button-list" :class="{ 'active': buscador && buscador.length > 0 }">
                        <div>
                            <button v-for="(item, index) in usuariosDataBuscador" :key="index" @click="buscador = null,
                                userSelected = item,
                                dataToSend.usuario_id = item.usuario_id">{{
                                    item.nombre }} {{
                                    item.apellido
                                }}</button>
                        </div>
                    </div>
                </div>
            </div>

            <h4>Usuario seleccionado: {{ userSelected.nombre }} {{ userSelected.apellido }}</h4>

            <div>
                <label for="fecha">Fecha</label>
                <input type="date" id="fecha" v-model="dataToSend.fecha">
            </div>

            <div>
                <label for="searcher">Buscador de productos</label>
                <input type="text" v-model="buscadorPrd" id="searcher"
                    placeholder="Buscar por nombre, correo o apellido">

                <div class="height-ancor" v-if="buscadorPrd && buscadorPrd.length > 0">
                    <div class="button-list">
                        <button v-for="(item, index) in productsData" :key="index" @click="addProduct(item)">
                            {{ item.nombre }}
                        </button>
                    </div>
                </div>

                <div class="productWrapper" v-for="(item, index) in dataToSend.productos" :key="index">
                    <p>{{ item.nombre }} <span style="color: #888;">(Stock: {{ item.stock }})</span></p>
                    <input
                        type="number"
                        placeholder="Cantidad"
                        v-model.number="item.cantidad"
                        :min="1"
                        :max="item.stock"
                        @input="item.cantidad = Math.max(1, Math.min(item.cantidad, item.stock))"
                    >
                    <p>${{ item.precio }}</p>
                    <p v-if="item.cantidad > 0">${{ (item.cantidad * Number(item.precio)).toFixed(2) }}</p>
                    <button @click="deleteOnProduct(index)">
    
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor"
                            stroke-linecap="round" stroke-linejoin="round" width="24" height="24" stroke-width="2">
                            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0"></path>
                            <path d="M9 12l6 0"></path>
                        </svg>
                    </button>
                </div>
            </div>

            <div>
                <label for="number">Total</label>
                <input type="number" id="number" v-model="dataToSend.total" disabled>
            </div>

            <div>
                <label for="stock">Cantidad</label>
                <input type="number" id="stock" v-model="dataToSend.cantidad_art" disabled>
            </div>

            <button @click="submitData" :disabled="!dataToSend.usuario_id || !dataToSend.productos.length">Guardar</button>
        </div>
    </dialog>
</template>
<style scoped lang="scss">
dialog {
    margin: auto;
    width: min(100%, 400px);
}

.container-modal {
    display: grid;

    div {
        display: grid;
    }
}

.user-search-container {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
    max-width: 400px;
    margin: auto;
    padding: 1rem;
}

.search-label {
    font-weight: bold;
    font-size: 0.95rem;
    color: #333;
}

.search-input {
    padding: 0.5rem 0.75rem;
    border: 1px solid #ccc;
    border-radius: 0.5rem;
    font-size: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    transition: border-color 0.3s;
}

.search-input:focus {
    border-color: #007BFF;
    outline: none;
}

.height-ancor {
    height: .9375rem;
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
    background-color: #181818;
}

.button-list.active {
    grid-template-rows: 1fr;
}

.user-button {
    padding: 0.5rem 1rem;
    background-color: #f0f0f0;
    border: 1px solid #ddd;
    border-radius: 0.4rem;
    text-align: left;
    font-size: 0.95rem;
    cursor: pointer;
    transition: background-color 0.3s;
}

.user-button:hover {
    background-color: #e0e0e0;
}

.productWrapper {
    display: grid;
    grid-template-columns: repeat(4, 1fr);

    p:first-of-type {
        grid-column: 1 / -1;
    }
}
</style>
