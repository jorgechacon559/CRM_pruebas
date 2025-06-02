# Sistema de gestión de ventas - Dashboard - Backend & Frontend

## Tabla de contenidos

- [Descripción general](#descripción-general)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Migraciones y base de datos](#migraciones-y-base-de-datos)
- [Ejecución](#ejecución)
- [Funcionalidades](#funcionalidades)
- [Endpoints principales](#endpoints-principales)
- [Seguridad y roles](#seguridad-y-roles)
- [Manejo de usuarios](#manejo-de-usuarios)
- [Frontend: UX y notificaciones](#frontend-ux-y-notificaciones)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Créditos y licencia](#créditos-y-licencia)

---

## Descripción general

Este proyecto es una plataforma integral de gestión de ventas con:

- **Backend** en Python (Flask) con autenticación JWT, roles de usuario, baja lógica, API RESTful, gestión de usuarios, productos y ventas, y chatbot integrado.
- **Frontend** en Vue 3, con dashboard interactivo, autenticación, gestión de usuarios, productos y ventas, notificaciones tipo toast, y diseño responsivo.

---

## Requisitos

- Python 3.8+
- Node.js 16+
- MySQL 5.7+
- npm/yarn

---

## Instalación

### Backend

1. Clona el repositorio y entra al directorio del backend:

    ```sh
    cd proyecto_back_end
    ```

2. Instala las dependencias de Python:

    ```sh
    pip install -r requirements.txt
    ```

3. Crea la base de datos en MySQL:

    ```sql
    CREATE DATABASE storedb CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

4. Configura tu archivo `.env` con los datos de conexión:

    ```
    DB_USER=root
    DB_PASSWORD=root
    DB_HOST=localhost
    DB_NAME=storedb
    DB_PORT=3306
    SECRET_KEY=your_secret_key
    JWT_SECRET_KEY=your_jwt_secret_key
    ```

### Frontend

1. Entra al directorio del frontend:

    ```sh
    cd proyecto_front_end
    ```

2. Instala las dependencias de Node.js:

    ```sh
    npm install
    ```

3. Configura el archivo `.env` con la URL del backend:

    ```
    VITE_API_URL=http://localhost:5000/api
    ```

---

## Estructura del proyecto

```
proyecto_back_end/
    app/
        controllers/
        models/
        routes/
        ...
    migrations/
    tests/
    requirements.txt
    .env
    config.py

proyecto_front_end/
    src/
        components/
        api/
        stores/
        router/
        assets/
        App.vue
        main.js
    public/
    .env
    package.json
    vite.config.js
```

---

## Configuración

- Variables de entorno para backend y frontend.
- Configuración de CORS y JWT.
- Personalización de puertos y rutas según entorno.

---

## Migraciones y base de datos

Inicializa y ejecuta las migraciones para crear las tablas:

```sh
flask db init
flask db migrate -m "tablas con relaciones"
flask db upgrade
```

---

## Ejecución

### Backend

```sh
flask run
```

### Frontend

```sh
npm run dev
```

---

## Funcionalidades

### Backend

- 🔐 **Autenticación JWT:** Registro, login, refresh y logout seguro.
- 👤 **Roles:** Soporte para roles `admin` y `usuario`. Solo los admins pueden acceder a la gestión de usuarios.
- 🛑 **Baja lógica:** Los usuarios pueden ser dados de baja (soft delete), cambiando su estado y email.
- 🛡️ **Ascenso de usuario:** Un admin puede ascender a otro usuario a admin, previa confirmación de contraseña.
- 🛒 **Gestión:** CRUD de productos, usuarios y ventas.
- 🤖 **Chatbot:** Consultas sobre ventas, productos y soporte.
- 📦 **API RESTful** para integración con el frontend.
- 📈 **Métricas:** Endpoints para estadísticas y reportes.

### Frontend

- 🖥️ **Dashboard:** Visualización de métricas y gráficas de ventas.
- 👤 **Gestión de usuarios:** Alta, edición, baja lógica y ascenso de rol.
- 🛍️ **Gestión de productos y ventas:** CRUD completo.
- 💬 **Chatbot:** Interfaz de chat en tiempo real.
- 🔒 **Autenticación:** Formularios de login y registro, manejo de tokens y refresh.
- 🎨 **UI/UX:** Diseño responsivo y moderno.
- ✅ **Notificaciones toast:** Mensajes de éxito y error con toasts personalizados (verde para éxito, rojo para errores o bajas).

---

## Endpoints principales

| Método | Ruta                                 | Descripción                        |
|--------|--------------------------------------|------------------------------------|
| POST   | /api/login                           | Autenticación de usuario           |
| POST   | /api/refresh                         | Refrescar token JWT                |
| POST   | /api/registrar                       | Registro de usuario                |
| GET    | /api/usuarios                        | Listar usuarios (solo admin)       |
| PUT    | /api/usuarios/<id>/baja              | Baja lógica de usuario (admin)     |
| PUT    | /api/usuarios/<id>/hacer-admin       | Ascender usuario a admin (admin)   |
| GET    | /api/productos                       | Listar productos                   |
| POST   | /api/productos                       | Crear producto                     |
| PUT    | /api/productos/<id>                  | Editar producto                    |
| DELETE | /api/productos/<id>                  | Eliminar producto (baja lógica)    |
| GET    | /api/ventas                          | Listar ventas                      |
| POST   | /api/ventas                          | Crear venta                        |
| GET    | /api/chatbot                         | Consultar chatbot                  |
| GET    | /api/ventas/data                     | Obtener métricas de ventas         |

---

## Seguridad y roles

- **Contraseñas:** Hasheadas con bcrypt.
- **Roles:**  
  - `admin`: Acceso total a usuarios, productos y ventas.
  - `usuario`: Acceso solo a sus propios datos y ventas.
- **Protección de rutas:**  
  - Solo admins pueden acceder a `/usuarios` y realizar bajas o ascensos.
  - Validación de rol en backend y frontend.
- **Tokens JWT:**  
  - Acceso y refresh token, guardados en sessionStorage.
  - Middleware para refrescar token automáticamente en frontend.
- **Baja lógica:**  
  - El usuario dado de baja no puede volver a iniciar sesión.
  - El email se modifica para evitar duplicados (`email_baja_<id>`).

---

## Manejo de usuarios

- **Registro:**  
  - Validación de email único.
  - Contraseña fuerte (mínimo 8 caracteres, mayúsculas, minúsculas, número y símbolo).
- **Login:**  
  - Devuelve datos completos del usuario (incluyendo email y rol).
- **Ascenso a admin:**  
  - Modal de confirmación, requiere contraseña del admin actual.
  - Toast verde al éxito, mensaje de error si la contraseña es incorrecta.
- **Baja lógica:**  
  - Solo admins pueden dar de baja.
  - Toast rojo al dar de baja, mensaje de error si falla.

---

## Frontend: UX y notificaciones

- **Toasts personalizados:**  
  - Componente `Toast.vue` reutilizable.
  - Verde para éxito (`success`), rojo para errores o bajas (`error`).
  - Cierre automático y manual.
- **Validaciones visuales:**  
  - Inputs con feedback visual para errores.
  - Mensajes claros en formularios de login y registro.
- **Paginación y búsqueda:**  
  - Listados paginados de usuarios y ventas.
- **Modal de ascenso:**  
  - Confirmación con contraseña antes de ascender a admin.

---

## Pruebas

- Pruebas unitarias y de integración en `tests/` (backend).
- Scripts de test para frontend (`npm test` o `yarn test`).

---

## Despliegue

- Uso de variables de entorno (.env)
- Soporte para Gunicorn y Nginx (opcional)
- Hosting sugerido: Render, Heroku, DigitalOcean, Vercel (frontend)
- Configuración de Docker (opcional)

---

## Créditos y licencia

**Autores:**  
Quasar y Pulsar

**Año:** 2025  
**Licencia:** MIT / GPL / Privado

---