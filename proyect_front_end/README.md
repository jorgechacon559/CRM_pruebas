# project_front_end

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

📄=======================================
📊 DOCUMENTACIÓN DEL PROYECTO
📈 DASHBOARD DE VENTAS CON LOGIN/CHATBOT
=======================================📄

1️⃣ INTRODUCCIÓN
---------------
🧩 Nombre del proyecto: Dashboard de Ventas con Autenticación y Chatbot  
🛠️ Tecnologías utilizadas: Vue.js (frontend), Flask (backend),MySQL, API de Chatbot  
🎯 Propósito: Proporcionar una interfaz web para visualizar métricas de ventas, gestionar accesos mediante autenticación y consultar un chatbot para soporte o reportes rápidos.

2️⃣ ESTRUCTURA DEL PROYECTO
---------------------------
🖥️ Frontend (Vue.js):
  /frontend
    ├── public/
    ├── src/
    │   ├── assets/
    │   ├── components/
    │   ├── views/
    │   ├── router/
    │   └── App.vue
    ├── package.json
    └── vite.config.js o vue.config.js

🧠 Backend (Flask):
  /backend
    ├── app/
    │   ├── __init__.py
    │   ├── routes/
    │   ├── models/
    │   ├── auth/
    │   └── chatbot/
    ├── run.py
    └── requirements.txt

3️⃣ INSTALACIÓN Y CONFIGURACIÓN
------------------------------
⚙️ REQUISITOS:
- Node.js y npm
- Python 3.8+
- pip
- (Opcional) Docker

📥 INSTALACIÓN:

Frontend:
  cd frontend
  npm install
  npm run dev

Backend:
  cd backend
  python -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  python run.py

4️⃣ FUNCIONALIDADES
------------------
🔐 LogIn / Autenticación:
  * Inicio de sesión
  * Protección de rutas
  * Manejo de tokens o sesiones

📊 Dashboard:
  * Visualización de gráficas de ventas
  * Filtros por fecha o categoría
  * Exportación de datos

🤖 Chatbot:
  * Respuestas a preguntas frecuentes
  * Consultas sobre ventas y stock
  * Puede conectarse a una API externa o usar lógica local

5️⃣ API ENDPOINTS (FLASK)
------------------------
| 📡 Método | 📍 Ruta             | 📌 Descripción                |
|----------|--------------------|------------------------------|
| POST     | /login             | Autenticación de usuario     |
| GET      | /dashboard/data    | Datos para gráficas          |
| POST     | /chatbot/message   | Enviar mensaje al chatbot    |
| GET      | /user/profile      | Obtener perfil de usuario    |

6️⃣ SEGURIDAD
------------
🔒 Contraseñas hasheadas con bcrypt  
🪪 Uso de tokens JWT o sesiones  
🌐 Configuración de CORS para integración frontend-backend

7️⃣ DESPLIEGUE
-------------
🧾 Uso de variables de entorno (.env)  
🚀 Despliegue con Gunicorn y Nginx (opcional)  
🛠️ Compilación del frontend: npm run build  
🌍 Hosting sugerido: Render, Heroku, DigitalOcean

8️⃣ DIAGRAMAS 
----------------------
🖼️ Front-End  
🔗 https://www.mermaidchart.com/app/projects/bc49abfc-b1d8-41f7-a4a0-4a9a5d5044f6/diagrams/e52b2d5b-0e7c-4b05-8818-c1de074c3c63/version/v0.1/edit  
🖼️ Back-end  
🔗 https://www.mermaidchart.com/app/projects/bc49abfc-b1d8-41f7-a4a0-4a9a5d5044f6/diagrams/06265c28-cbec-4f7d-800b-ed21fbc79cc4/version/v0.1/edit

9️⃣ CRÉDITOS Y LICENCIA
----------------------
✍️ Autores: 
Jesús Eduardo Valenzuela Urióstegui  
Reynaldo Manzanilla  
Oscar Alonso Medina Silva  
Juan Antonio Vázquez Velázquez  
Carlos Enrique Aguilar Maza  
📅 Año: 2025  
📜 Licencia: MIT / GPL / Privado
