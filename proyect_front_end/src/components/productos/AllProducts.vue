<script setup>
import { reactive, onMounted, computed, ref, watch } from 'vue';
import { useProductsStore } from '@/stores/products';
import ModalGen from './ModalGen.vue';

const headers = reactive(['nombre', 'descripcion', 'precio', 'stock']);
const paginadorData = reactive({
    currentPage: 1,
    totalPages: undefined,
    itemsPerPage: 15,
})

const products = useProductsStore();
const productsData = computed(() => {
    const data = products.data;
    if(!data) return
    paginadorData.totalPages = Math.ceil(data.length / paginadorData.itemsPerPage);

    const start = (paginadorData.currentPage - 1) * paginadorData.itemsPerPage;
    const end = start + paginadorData.itemsPerPage;

    return data.slice(start, end);
});

watch(() => paginadorData.currentPage,
(newVal) => {
    if((newVal === null || newVal === undefined || newVal === '') || newVal < 1) {
        paginadorData.currentPage = 1;
    } else if (newVal > paginadorData.totalPages) {
        paginadorData.currentPage = paginadorData.totalPages;
    }
})

const modalGenFather = ref(null);

const paginatorState = (toRight) => {
    paginadorData.currentPage = toRight ?
        Math.min(paginadorData.totalPages, ++paginadorData.currentPage) :
        Math.max(1, --paginadorData.currentPage)
}

const openModal = () => {
    modalGenFather.value.openModal();
}

const getInfo = async () => {
    await products.getAllInfoPrd('productos');
}

const toAdded = (item) => {
    products.setAdded(item)
    openModal();
}

const deleteItem = async (id) => {
    try {
        const response = await products.deleteItemPrd({ 'option': 'productos', id })
        if (response.message !== 'Producto dado de baja') throw { message: 'Error al eliminar producto' };
        getInfo();

    } catch (error) {
        console.log(message)
    }
}

onMounted(async () => {
    await getInfo();
})

</script>
<template>
    <div class="container-all-products">
        <ModalGen ref="modalGenFather" @allFine="getInfo" />
        <h2>Todos los productos:</h2>
        <button @click="openModal">Crear producto</button>
        <div class="table">
            <div class="table-heads">
                <div v-for="(head, index) in headers" :key="index" :class="{ 'centered': index > 1 }">
                    <p>{{ head }}</p>
                </div>
            </div>
            <div class="table-data">
                <div class="table-row" v-for="(item, index) in productsData" :key="index">
                    <div>
                        <p>{{ item.nombre }}</p>
                    </div>
                    <div>
                        <p>{{ item.descripcion }}</p>
                    </div>
                    <div class="centered">
                        <p>${{ item.precio }}</p>
                    </div>
                    <div class="centered">
                        <p>{{ item.stock }}</p>
                    </div>
                    <button class="btn-edit" @click="toAdded(item)">
                        <svg width="15" height="20" viewBox="0 0 20 20" fill="none"
                            stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <path d="M4 13.5V16h2.5l7.06-7.06a1.5 1.5 0 0 0-2.12-2.12L4 13.5z"/>
                            <path d="M14.5 6.5l-2-2"/>
                        </svg>
                    </button>
                    <button class="btn-delete" @click="deleteItem(item.producto_id)">
                        <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <line x1="5" y1="5" x2="15" y2="15"/>
                            <line x1="15" y1="5" x2="5" y2="15"/>
                        </svg>
                    </button>
                </div>
            </div>

            <div class="paginator">
                <div class="paginator-controls">
                    <button @click="paginatorState(false)">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24"
                            height="24">
                            <path
                                d="M12 2a10 10 0 0 1 .324 19.995l-.324 .005l-.324 -.005a10 10 0 0 1 .324 -19.995zm.707 5.293a1 1 0 0 0 -1.414 0l-4 4a1.048 1.048 0 0 0 -.083 .094l-.064 .092l-.052 .098l-.044 .11l-.03 .112l-.017 .126l-.003 .075l.004 .09l.007 .058l.025 .118l.035 .105l.054 .113l.043 .07l.071 .095l.054 .058l4 4l.094 .083a1 1 0 0 0 1.32 -1.497l-2.292 -2.293h5.585l.117 -.007a1 1 0 0 0 -.117 -1.993h-5.586l2.293 -2.293l.083 -.094a1 1 0 0 0 -.083 -1.32z">
                            </path>
                        </svg>
                    </button>

                    <p>{{ paginadorData.currentPage }} / {{ paginadorData.totalPages }}</p>

                    <button @click="paginatorState(true)">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24"
                            height="24">
                            <path
                                d="M12 2l.324 .005a10 10 0 1 1 -.648 0l.324 -.005zm.613 5.21a1 1 0 0 0 -1.32 1.497l2.291 2.293h-5.584l-.117 .007a1 1 0 0 0 .117 1.993h5.584l-2.291 2.293l-.083 .094a1 1 0 0 0 1.497 1.32l4 -4l.073 -.082l.064 -.089l.062 -.113l.044 -.11l.03 -.112l.017 -.126l.003 -.075l-.007 -.118l-.029 -.148l-.035 -.105l-.054 -.113l-.071 -.111a1.008 1.008 0 0 0 -.097 -.112l-4 -4z">
                            </path>
                        </svg>
                    </button>
                </div>

                <input type="number" :min="1" :max="paginadorData.totalPages" v-model="paginadorData.currentPage">
            </div>
        </div>
    </div>
</template>
<style scoped lang="scss">
.table {
    display: grid;
    width: fit-content;

    gap: .125rem;

    &-heads {
        display: grid;
        text-transform: capitalize;

        grid-template-columns: 18.75rem 37.5rem 6.25rem 6.25rem 3.125rem 3.125rem;
        gap: .125rem;
    }

    &-data {
        display: grid;
        gap: .125rem;
    }

    &-row {
        display: grid;
        grid-template-columns: 18.75rem 37.5rem 6.25rem 6.25rem 3.125rem 3.125rem;
        gap: .125rem;

        >div {
            display: -webkit-box;
            -webkit-box-orient: vertical;
            box-orient: vertical; /* estándar, opcional */
            -webkit-line-clamp: 1;
            line-clamp: 1; /* estándar */
            overflow: hidden;
            white-space: normal;
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

.btn-edit {
  background: #f1f5ff;
  border: 1.5px solid #b6d0fa;
  color: #2563eb;
  border-radius: 50%;
  width: 2.5rem;
  height: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  margin-right: 0.5rem;
  transition: background 0.2s, border 0.2s, color 0.2s;
  box-shadow: 0 1px 4px rgba(37,99,235,0.04);
  font-size: 1.3rem;
}
.btn-edit:hover {
  background: #2563eb;
  color: #fff;
  border-color: #2563eb;
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