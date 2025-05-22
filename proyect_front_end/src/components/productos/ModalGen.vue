<script setup>
import { ref, defineExpose, reactive, computed, watch } from 'vue';
import { useProductsStore } from '@/stores/products';

const modalGen = ref(null);

// Emitir eventos
const emit = defineEmits(['allFine']);

// Store y estado reactivo
const products = useProductsStore();
const productsAdded = computed(() => products.added);

const dataToSend = reactive({
    producto_id: null,
    descripcion: null,
    nombre: null,
    precio: null,
    stock: null
});

// Rellenar el formulario automáticamente si hay un producto seleccionado
watch(productsAdded, (newProduct) => {
    if (newProduct) {
        dataToSend.producto_id = newProduct.producto_id;
        dataToSend.descripcion = newProduct.descripcion;
        dataToSend.nombre = newProduct.nombre;
        dataToSend.precio = newProduct.precio;
        dataToSend.stock = newProduct.stock;
    } else {
        resetForm();
    }
});

// Métodos del modal
const openModal = () => {
    modalGen.value.showModal();
    requestAnimationFrame(() => {
        window.addEventListener('click', clickOutside);
        window.addEventListener('keydown', handleEsc);
    });
};

const closeModal = () => {
    modalGen.value?.close();
    window.removeEventListener('click', clickOutside);
    window.removeEventListener('keydown', handleEsc);

    // Limpiar producto seleccionado en el store y formulario
    products.setAdded(null);
    resetForm();
};

// Resetea los datos del formulario
const resetForm = () => {
    dataToSend.producto_id = null;
    dataToSend.descripcion = null;
    dataToSend.nombre = null;
    dataToSend.precio = null;
    dataToSend.stock = null;
};

// Detectar clic fuera del modal
const clickOutside = (e) => {
    if (!modalGen.value?.open) return;
    const rect = modalGen.value.getBoundingClientRect();
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
    try {
        const item = { ...dataToSend };
        const ruta = item.producto_id ? 'editItemPrd' : 'addItemPrd';
        const option = item.producto_id ? `productos/${item.producto_id}` : 'productos'
        const response = await products[ruta]({ option, item });
        if (['Producto registrado', 'Producto actualizado'].includes(response.message)) {
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

<template>
    <dialog ref="modalGen">
        <div class="container-modal">
            <div>
                <label for="name">Nombre</label>
                <input type="text" id="name" v-model="dataToSend.nombre">
            </div>
            <div>
                <label for="description">Descripción</label>
                <textarea id="description" v-model="dataToSend.descripcion"></textarea>
            </div>
            <div>
                <label for="price">Precio</label>
                <input type="number" id="price" v-model="dataToSend.precio">
            </div>
            <div>
                <label for="stock">Stock</label>
                <input type="number" id="stock" v-model="dataToSend.stock">
            </div>

            <button @click="submitData">Guardar</button>
        </div>
    </dialog>
</template>
<style scoped lang="scss">
dialog {
    margin: auto;
}

.container-modal {
    min-width: 18.75rem;

    >div {
        display: grid;
    }
}

textarea {
    resize: none;
}
</style>