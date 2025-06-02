<script setup>
import { reactive, onMounted, computed, ref, watch, onBeforeUnmount } from 'vue';
import { useUsuariosStore } from '@/stores/usuarios';
import api from '@/api/axios';
import Toast from '@/components/Toast.vue';

const showToast = ref(false)
const toastMessage = ref('')
const toastType = ref('success')

function showSuccessToast(msg) {
  toastMessage.value = msg
  toastType.value = 'success'
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2500)
}

function showErrorToast(msg) {
  toastMessage.value = msg
  toastType.value = 'error'
  showToast.value = true
  setTimeout(() => { showToast.value = false }, 2500)
}

const headers = reactive(['Nombre', 'Apellido', 'Correo', 'Rol', 'Acciones']);
const paginadorData = reactive({
    currentPage: 1,
    totalPages: undefined,
    itemsPerPage: 15,
});
const pageInput = ref('');
watch(() => paginadorData.currentPage, (val) => {
  pageInput.value = val ? val.toString() : '';
});
const usuarios = useUsuariosStore();
const usuariosData = computed(() => {
    const data = usuarios.data;
    if(!data) return;
    paginadorData.totalPages = Math.max(1, Math.ceil(data.length / paginadorData.itemsPerPage));
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
});
const paginatorState = (toRight) => {
    paginadorData.currentPage = toRight ?
        Math.min(paginadorData.totalPages, ++paginadorData.currentPage) :
        Math.max(1, --paginadorData.currentPage);
};
const validateAndGoToPage = () => {
    const page = parseInt(pageInput.value, 10);
    if (!isNaN(page) && page >= 1 && page <= paginadorData.totalPages) {
        paginadorData.currentPage = page;
    }
};
let identity = sessionStorage.getItem('user');
identity = identity ? JSON.parse(identity) : null;
const getInfo = async () => {
    await usuarios.getAllInfoUsr('usuarios');
};
onMounted(async () => {
    await getInfo();
});

// Modal para upgrade
const showUpgradeModal = ref(false);
const usuarioUpgradeId = ref(null);
const adminPassword = ref('');
const upgradeError = ref('');

const confirmarUpgrade = (usuario_id) => {
    usuarioUpgradeId.value = usuario_id;
    adminPassword.value = '';
    upgradeError.value = '';
    showUpgradeModal.value = true;
    setTimeout(() => {
      document.addEventListener('keydown', handleEsc);
    }, 0);
};

const cancelarUpgrade = () => {
    showUpgradeModal.value = false;
    usuarioUpgradeId.value = null;
    adminPassword.value = '';
    upgradeError.value = '';
    document.removeEventListener('keydown', handleEsc);
};

const handleEsc = (e) => {
    if (e.key === 'Escape') cancelarUpgrade();
};

const modalOverlayClick = (e) => {
    if (e.target.classList.contains('modal-overlay')) cancelarUpgrade();
};

onBeforeUnmount(() => {
    document.removeEventListener('keydown', handleEsc);
});

const realizarUpgrade = async () => {
    upgradeError.value = '';
    try {
        const adminEmail = identity.email;
        if (!adminEmail) {
            upgradeError.value = 'No se encontró el correo del administrador actual.';
            return;
        }
        const response = await api.post('/login', {
            email: adminEmail,
            password: adminPassword.value
        });
        if (response.data && response.data.access_token) {
            await api.put(`/usuarios/${usuarioUpgradeId.value}/hacer-admin`, {}, {
                headers: { Authorization: `Bearer ${response.data.access_token}` }
            });
            await getInfo();
            cancelarUpgrade();
            showSuccessToast('Usuario ascendido a Administrador correctamente');
        } else {
            upgradeError.value = 'Contraseña incorrecta';
        }
    } catch (e) {
        upgradeError.value = 'Contraseña incorrecta o error de autenticación';
    }
};

const eliminarUsuario = async (usuario_id) => {
    try {
        const token = sessionStorage.getItem("token");
        await api.put(`/usuarios/${usuario_id}/baja`, {}, {
            headers: { Authorization: `Bearer ${token}` }
        });
        await getInfo();
        showErrorToast('Usuario dado de baja');
    } catch (e) {
        showErrorToast('No se pudo eliminar al usuario');
    }
};
</script>

<template>
    <div class="container-all-sails content">
        <h2>Todos los usuarios:</h2>
        <div class="table table-bg">
            <div class="table-heads">
                <div v-for="(head, index) in headers" :key="index">
                    <p>{{ head }}</p>
                </div>
            </div>
            <div class="table-data">
                <div class="table-row" v-for="(item, index) in usuariosData" :key="index"
                     :style="{opacity: item.baja ? 0.5 : 1}">
                    <div>
                        <p>{{ item.nombre }}</p>
                    </div>
                    <div>
                        <p>{{ item.apellido }}</p>
                    </div>
                    <div>
                        <p>{{ item.email }}</p>
                    </div>
                    <div>
                        <p>{{ item.rol }}</p>
                    </div>
                    <div class="acciones">
                        <!-- Botón upgrade a admin -->
                        <button
                          v-if="identity && identity.rol === 'admin' && item.rol !== 'admin' && !item.baja"
                          class="btn-circular btn-upgrade"
                          @click="confirmarUpgrade(item.usuario_id)"
                          title="Hacer admin"
                        >
                          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#15803d" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="10" cy="10" r="9" stroke="#15803d" stroke-width="2" fill="#e6fbe6"/>
                            <polyline points="5 12 10 7 15 12" stroke="#15803d" stroke-width="2" fill="none"/>
                          </svg>
                        </button>
                        <!-- Botón eliminar -->
                        <button
                          v-if="identity && identity.rol === 'admin' && !item.baja"
                          class="btn-circular btn-delete"
                          @click="eliminarUsuario(item.usuario_id)"
                          title="Eliminar usuario"
                        >
                          <svg width="20" height="20" viewBox="0 0 20 20" fill="none" stroke="#d32f2f" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                            <circle cx="10" cy="10" r="9" stroke="#d32f2f" stroke-width="2" fill="#fff0f0"/>
                            <line x1="5" y1="5" x2="15" y2="15"/>
                            <line x1="15" y1="5" x2="5" y2="15"/>
                          </svg>
                        </button>
                        <span v-if="item.baja" style="color: #d32f2f;">Inactivo</span>
                    </div>
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

                <input
                    type="text"
                    placeholder="Ir a página..."
                    v-model="pageInput"
                    @keyup.enter="validateAndGoToPage"
                    @blur="validateAndGoToPage"
                >            
            </div>
        </div>
    </div>
    <!-- Modal de confirmación para upgrade -->
    <div v-if="showUpgradeModal" class="modal-overlay" @mousedown="modalOverlayClick">
      <div class="modal-content" @mousedown.stop>
        <h3>Confirmar ascenso a Administrados</h3>
        <p>Para continuar, ingresa tu contraseña:</p>
        <input type="password" v-model="adminPassword" placeholder="Contraseña actual" />
        <div class="modal-actions">
          <button @click="realizarUpgrade" class="btn-upgrade">Confirmar</button>
          <button @click="cancelarUpgrade" class="btn-delete">Cancelar</button>
        </div>
        <p v-if="upgradeError" style="color:#d32f2f;">{{ upgradeError }}</p>
      </div>
    </div>
    <Toast :show="showToast" :message="toastMessage" :type="toastType" @close="showToast = false" />
</template>

<style scoped lang="scss">
.table {
    display: grid;
    width: fit-content;
    gap: .125rem;

    &-heads {
        display: grid;
        text-transform: capitalize;
        grid-template-columns: 10rem 10rem 18rem 7rem 14rem;
        gap: .125rem;
    }

    &-data {
        display: grid;
        gap: .125rem;
    }

    &-row {
        display: grid;
        grid-template-columns: 10rem 10rem 18rem 7rem 14rem;
        gap: .125rem;

        >div {
            display: -webkit-box;
            -webkit-box-orient: vertical;
            -webkit-line-clamp: 1;
            line-clamp: 1;
            overflow: hidden;
        }
        .acciones {
            display: flex;
            gap: 0.5rem;
            align-items: center;
        }
        .btn-circular {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            border: none;
            display: grid;
            place-items: center;
            padding: 0;
            background: transparent;
            transition: background 0.2s;
        }
        .btn-upgrade {
            &:hover {
                background: #e6fbe6;
            }
        }
        .btn-delete {
            &:hover {
                background: #ffeaea;
            }
        }
    }
}

.table-bg {
    background: #fff;
    border-radius: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    padding: 1.5rem 2rem;
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

.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: #fff;
  border-radius: 1rem;
  padding: 2rem;
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
  min-width: 320px;
  max-width: 90vw;
}
.modal-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
  justify-content: flex-end;
}
</style>