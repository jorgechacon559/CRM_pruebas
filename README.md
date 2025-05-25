# Dashboard de Ventas - Backend & Frontend

## Tabla de Contenidos

- [Descripción General](#descripción-general)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Configuración](#configuración)
- [Migraciones y Base de Datos](#migraciones-y-base-de-datos)
- [Ejecución](#ejecución)
- [Funcionalidades](#funcionalidades)
- [Endpoints Principales](#endpoints-principales)
- [Seguridad](#seguridad)
- [Pruebas](#pruebas)
- [Despliegue](#despliegue)
- [Créditos y Licencia](#créditos-y-licencia)

---

## Descripción General

Este proyecto es una plataforma completa de gestión de ventas que incluye:

- **Backend** en Python (Flask) con autenticación JWT, API RESTful, gestión de usuarios, productos y ventas, y un chatbot integrado.
- **Frontend** moderno (React) con dashboard interactivo, visualización de métricas, autenticación y chat en tiempo real.

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
    CREATE DATABASE STOREDB CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    ```

4. Configura tu archivo `.env` con los datos de conexión:

    ```
    DB_USER=root
    DB_PASSWORD=root
    DB_HOST=localhost
    DB_NAME=STOREDB
    DB_PORT=3306
    DB_DRIVER=mysql
    SECRET_KEY=your_secret_key
    ```

### Frontend

1. Entra al directorio del frontend:

    ```sh
    cd proyecto_front_end
    ```

2. Instala las dependencias de Node.js:

    ```sh
    npm install
    # o
    yarn install
    ```

3. Configura el archivo `.env` con la URL del backend:

    ```
    REACT_APP_API_URL=http://localhost:5000/api
    ```

---

## Estructura del Proyecto

```
proyecto_back_end/
    app/
        controllers/
        models/
        routes/
        schemas/
        services/
        utils/
        static/
        templates/
    migrations/
    tests/
    requirements.txt
    .env
    config.py
    wsgi.py

proyecto_front_end/
    src/
        components/
        pages/
        services/
        hooks/
        utils/
        assets/
        App.js
        index.js
    public/
    .env
    package.json
    README.md
```

---

## Configuración

- Variables de entorno para backend y frontend.
- Configuración de CORS y JWT.
- Personalización de puertos y rutas según entorno.

---

## Migraciones y Base de Datos

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
npm start
# o
yarn start
```

---

## Funcionalidades

### Backend

- 🔐 **Autenticación:** Registro, inicio de sesión, protección de rutas, manejo de tokens JWT.
- 🛒 **Gestión:** CRUD de productos, usuarios y ventas.
- 🤖 **Chatbot:** Consultas sobre ventas, productos y soporte.
- 📦 **API RESTful** para integración con el frontend.
- 📈 **Métricas:** Endpoints para estadísticas y reportes.

### Frontend

- 🖥️ **Dashboard:** Visualización de métricas y gráficas de ventas.
- 👤 **Gestión de usuarios:** Alta, edición y baja lógica.
- 🛍️ **Gestión de productos y ventas:** CRUD completo.
- 💬 **Chatbot:** Interfaz de chat en tiempo real.
- 🔒 **Autenticación:** Formularios de login y registro.
- 🎨 **UI/UX:** Diseño responsivo y moderno.

---

## Endpoints Principales

| Método | Ruta                       | Descripción                        |
|--------|----------------------------|------------------------------------|
| POST   | /api/login                 | Autenticación de usuario           |
| POST   | /api/register              | Registro de usuario                |
| GET    | /api/usuarios              | Listar usuarios                    |
| GET    | /api/usuarios/<id>         | Obtener usuario por ID             |
| PUT    | /api/usuarios/<id>         | Editar usuario                     |
| DELETE | /api/usuarios/<id>         | Baja lógica de usuario             |
| GET    | /api/productos             | Listar productos                   |
| GET    | /api/productos/<id>        | Obtener producto por ID            |
| POST   | /api/productos             | Crear producto                     |
| PUT    | /api/productos/<id>        | Editar producto                    |
| DELETE | /api/productos/<id>        | Eliminar producto (baja lógica)    |
| GET    | /api/ventas                | Listar ventas                      |
| GET    | /api/ventas/<id>           | Obtener venta por ID               |
| POST   | /api/ventas                | Crear venta                        |
| POST   | /api/chatbot               | Consultar chatbot                  |
| GET    | /api/metrics               | Obtener métricas de ventas         |

---

## Seguridad

- Contraseñas hasheadas con bcrypt.
- Autenticación y autorización con JWT.
- CORS configurado para integración frontend-backend.
- Validación de datos y manejo de errores.
- Protección contra ataques comunes (CSRF, XSS, etc).

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

## Créditos y Licencia

**Autores:**  
Quasar y Pulsar

**Año:** 2025  
**Licencia:** MIT / GPL / Privado

---