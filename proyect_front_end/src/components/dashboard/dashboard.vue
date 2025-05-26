<template>
  <div class="dashboard p-6">
    <!-- Título centrado -->
    <h1 class="dashboard-title mb-8">Resumen de ventas</h1>

    <!-- Resumen general: 3 columnas -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div class="card">
        <h2>Productos disponibles</h2>
        <p>{{ resumen.total_productos }}</p>
      </div>
      <div class="card">
        <h2>Ventas esta semana</h2>
        <p>{{ resumen.ventas_semana }}</p>
      </div>
      <div class="card">
        <h2>Ingresos semanales</h2>
        <p>${{ resumen.ingresos_totales.toFixed(2) }}</p>
      </div>
    </div>

    <!-- Segunda fila: gráfico y producto más vendido lado a lado -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
      <div class="card">
        <h2>Ventas por día (última semana)</h2>
        <canvas ref="ventasChart" width="600" height="300"></canvas>
      </div>

      <div class="card flex flex-col justify-center">
        <h2>Producto más vendido</h2>
        <p v-if="productoTop.nombre" class="top-producto">
          {{ productoTop.nombre }} ({{ productoTop.cantidad_vendida }} unidades)
        </p>
        <p v-else class="no-data">No hay datos disponibles.</p>
      </div>
    </div>

    <!-- Última fila: ventas recientes (tabla) -->
    <div class="card">
      <h2>Ventas recientes</h2>
      <table>
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Usuario</th>
            <th>Total</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="venta in ventasRecientes" :key="venta.fecha + venta.usuario" class="table-row">
            <td>{{ venta.fecha }}</td>
            <td>{{ venta.usuario }}</td>
            <td>${{ venta.total.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Chart from 'chart.js/auto'

const resumen = ref({
  total_productos: 0,
  ventas_semana: 0,
  ingresos_totales: 0,
})

const ventasRecientes = ref([])
const ventasPorDia = ref([])
const productoTop = ref({})
const ventasChart = ref(null)

const fetchData = async () => {
  const [res1, res2, res3, res4] = await Promise.all([
    axios.get('http://127.0.0.1:5000/api/dashboard/summary'),
    axios.get('http://127.0.0.1:5000/api/dashboard/ventas-recientes'),
    axios.get('http://127.0.0.1:5000/api/dashboard/ventas-semana'),
    axios.get('http://127.0.0.1:5000/api/dashboard/producto-top'),
  ])
  resumen.value = res1.data
  ventasRecientes.value = res2.data
  ventasPorDia.value = res3.data
  productoTop.value = res4.data

  renderChart()
}

const renderChart = () => {
  if (ventasChart.value) {
    const ctx = ventasChart.value.getContext('2d')
    const dpr = window.devicePixelRatio || 1
    const rect = ventasChart.value.getBoundingClientRect()

    // Ajustar el tamaño del canvas para pantallas retina
    ventasChart.value.width = rect.width * dpr
    ventasChart.value.height = rect.height * dpr
    ctx.scale(dpr, dpr)

    new Chart(ctx, {
      type: 'bar', // Histograma
      data: {
        labels: ventasPorDia.value.map(d => d.fecha),
        datasets: [{
          label: 'Ingresos diarios',
          data: ventasPorDia.value.map(d => d.total),
          backgroundColor: 'rgba(35, 118, 201, 0.6)', // Color de fondo con opacidad
          borderColor: '#1d4ed8', // Color del borde
          borderWidth: 2,
          borderRadius: 5, // Bordes redondeados
          hoverBackgroundColor: 'rgba(35, 118, 201, 0.8)', // Color al pasar el mouse
          hoverBorderColor: '#1d4ed8',
          // Sombra
          shadowOffsetX: 0,
          shadowOffsetY: 2,
          shadowColor: 'rgba(0, 0, 0, 0.2)',
          shadowBlur: 4,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            labels: {
              color: '#2376c9'
            }
          },
          tooltip: {
            backgroundColor: '#1f2937',
            titleColor: '#2376c9',
            bodyColor: '#f9fafb',
            borderColor: '#2376c9',
            borderWidth: 1,
          }
        },
        scales: {
          x: {
            ticks: { color: '#2376c9' },
            grid: { color: 'rgba(203, 213, 225, 0.5)' } // Color de la cuadrícula más sutil
          },
          y: {
            min: 0,
            ticks: {
              color: '#2376c9',
              stepSize: 100
            },
            grid: { color: 'rgba(203, 213, 225, 0.5)' } // Color de la cuadrícula más sutil
          }
        },
        animation: {
          duration: 800, // Duración de la animación
          easing: 'easeOutBounce' // Efecto de la animación
        }
      }
    })
  }
}




onMounted(fetchData)
</script>

<style scoped>
.dashboard {
  background-color: #ffffff;
  color: #2376c9;
  min-height: 100vh;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Título centrado */
.dashboard-title {
  font-size: 2.5rem;
  font-weight: 700;
  text-align: center;
  color: #2376c9;
}

/* Tarjetas */
.card {
  background-color: #f9fbfe;
  color: #2376c9;
  border-left: 5px solid #2376c9;
  box-shadow: 0 2px 8px rgb(35 118 201 / 0.15);
  border-radius: 8px;
  padding: 20px;
  transition: transform 0.2s ease-in-out;
}

.card:hover {
  transform: translateY(-5px);
}

/* Encabezados dentro de las tarjetas */
.card h2 {
  margin-bottom: 12px;
  font-weight: 600;
  font-size: 1.25rem;
  color: #2376c9;
  border-bottom: 2px solid #2376c9;
  padding-bottom: 4px;
}

/* Tabla */
table {
  width: 100%;
  border-collapse: collapse;
  color: #2376c9;
}

th, td {
  padding: 12px 8px;
  border-bottom: 1px solid #cbd5e1;
  text-align: left;
}

th {
  background-color: #e1eefa;
  font-weight: 600;
}

.table-row:hover {
  background-color: #dbeafe;
  cursor: default;
}

/* Producto más vendido */
.top-producto {
  font-size: 1.5rem;
  font-weight: 700;
  color: #1d4ed8;
}

.no-data {
  font-style: italic;
  color: #94a3b8;
}


/* Canvas para el gráfico */
.card canvas {
  width: 100% !important;
  height: auto !important;
  max-height: 300px;
  display: block;
}
</style>
