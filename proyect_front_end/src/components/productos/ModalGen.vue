<template>
    <dialog ref="modalGen" class="modal-gen">
        <form class="container-modal" @submit.prevent="submitData">
            <h2 class="modal-title">{{ dataToSend.producto_id ? 'Editar producto' : 'Nuevo producto' }}</h2>
            <div class="form-group">
                <label for="name">Nombre</label>
                <input type="text" id="name" v-model="dataToSend.nombre" class="form-control" required>
            </div>
            <div class="form-group">
                <label for="description">Descripción</label>
                <textarea id="description" v-model="dataToSend.descripcion" class="form-control" rows="3" required></textarea>
            </div>
            <div class="form-group">
                <label for="price">Precio</label>
                <input type="number" id="price" v-model="dataToSend.precio" class="form-control" min="0" step="0.01" required>
            </div>
            <div class="form-group">
                <label for="stock">Stock</label>
                <input type="number" id="stock" v-model="dataToSend.stock" class="form-control" min="0" step="1" required>
            </div>
            <div class="modal-actions">
                <button type="submit" class="btn-primary">Guardar</button>
                <button type="button" class="btn-secondary" @click="closeModal">Cancelar</button>
            </div>
        </form>
    </dialog>
</template>

<script setup>
import { ref, defineExpose, reactive, computed, watch } from 'vue';
import { useProductsStore } from '@/stores/products';

const modalGen = ref(null);
const emit = defineEmits(['allFine']);
const products = useProductsStore();
const productsAdded = computed(() => products.added);

// Estado reactivo para el formulario del modal
const dataToSend = reactive({
    producto_id: null,
    descripcion: null,
    nombre: null,
    precio: null,
    stock: null
});

// Sincroniza el formulario con el producto seleccionado para editar
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

// Abre el modal y agrega listeners para cerrar con click fuera o ESC
const openModal = () => {
    modalGen.value.showModal();
    requestAnimationFrame(() => {
        window.addEventListener('click', clickOutside);
        window.addEventListener('keydown', handleEsc);
    });
};

// Cierra el modal y limpia listeners y formulario
const closeModal = () => {
    modalGen.value?.close();
    window.removeEventListener('click', clickOutside);
    window.removeEventListener('keydown', handleEsc);
    products.setAdded(null);
    resetForm();
};

// Limpia el formulario
const resetForm = () => {
    dataToSend.producto_id = null;
    dataToSend.descripcion = null;
    dataToSend.nombre = null;
    dataToSend.precio = null;
    dataToSend.stock = null;
};

// Cierra el modal si se hace click fuera del diálogo
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

// Cierra el modal si se presiona la tecla ESC
const handleEsc = (e) => {
    if (e.key === "Escape") closeModal();
};

// Envía el formulario para crear o editar producto
const submitData = async () => {
    try {
        const item = { ...dataToSend };
        const ruta = item.producto_id ? 'editItemPrd' : 'addItemPrd';
        const option = item.producto_id ? `productos/${item.producto_id}` : 'productos'
        const response = await products[ruta]({ option, item });
        if (['Producto registrado', 'Producto actualizado'].includes(response.message)) {
            const msg = item.producto_id ? '¡Producto actualizado correctamente!' : '¡Producto registrado correctamente!';
            emit('allFine', msg);
            closeModal();
        } else {
            throw new Error('Ha ocurrido un error');
        }
    } catch (error) {
        console.error(error.message);
    }
};

// Expone la función para abrir el modal al componente padre
defineExpose({
    openModal,
});
</script>

<style scoped lang="scss">
.modal-gen {
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
    width: 370px;
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

.btn-primary:hover {
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