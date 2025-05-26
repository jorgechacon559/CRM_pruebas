from dotenv import load_dotenv
from google import genai
import os
from flask import request, jsonify
from google.genai import types
from ..controllers.venta_controller import get_estadisticas_ventas
from ..controllers.producto_controller import get_all_productos

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY', 'AIzaSyCRcJxhvCHlho2GHmmQcKSpo9UInH1Q3A0')

def obtener_datos_ventas(data, get_estadisticas_ventas):
    """
    Obtiene y estructura los datos de ventas e inventario para el análisis del chatbot.
    """
    try:
        response, status = get_estadisticas_ventas()
        if status != 200:
            raise Exception("Error al obtener estadísticas")

        productos_mas_vendidos = {}
        productos_menos_vendidos = {}
        ventas_totales_mensuales = {}
        totales_anuales = {}

        nombres_meses = {
            1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril',
            5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto',
            9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
        }

        for mes_data in response:
            ventas_mes = mes_data['ventas_totales_mes']
            mes_num = int(ventas_mes['mes'].split('-')[1])
            nombre_mes = nombres_meses[mes_num]
            ventas_totales_mensuales[nombre_mes] = ventas_mes['total_ventas']

            for producto in mes_data['productos_mas_vendidos']:
                nombre = producto['nombre']
                totales_anuales[nombre] = totales_anuales.get(nombre, 0) + producto['total_vendidos']

        sorted_productos = sorted(totales_anuales.items(), key=lambda x: x[1], reverse=True)
        productos_mas_vendidos = dict(sorted_productos[:5])
        productos_menos_vendidos = dict(sorted_productos[-5:]) if len(sorted_productos) >= 5 else {}

        datos_ventas = {
            'productos_mas_vendidos': productos_mas_vendidos,
            'productos_menos_vendidos': productos_menos_vendidos,
            'ventas_totales_mensuales': ventas_totales_mensuales,
            'totales_anuales': totales_anuales
        }

        productos, _ = get_all_productos()
        inventario = []

        # Manejo robusto de la estructura de productos
        if isinstance(productos, str):
            productos_lista = []
        elif isinstance(productos, dict):
            productos_lista = productos.get("productos", productos)
        elif isinstance(productos, list):
            productos_lista = productos
        else:
            productos_lista = []

        for p in productos_lista:
            if isinstance(p, dict):
                inventario.append({
                    "producto_id": p.get("producto_id"),
                    "nombre": p.get("nombre"),
                    "stock": p.get("stock")
                })
        datos_ventas["inventario_actual"] = inventario

        return datos_ventas
    except Exception as e:
        print(f"Error en obtener_datos_ventas: {e}")
        return {}

def chat_bot(data, datos_ventas):
    """
    Llama al modelo Gemini para generar una respuesta de análisis de ventas.
    """
    try:
        cliente = genai.Client(api_key=api_key)
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash-preview-04-17",
            contents=f"""
            # Asistente Avanzado de Análisis de Ventas y Business Intelligence

            ## Rol y Objetivo
            Eres un analista experto en inteligencia de negocio especializado en ventas retail. Tu objetivo es proporcionar análisis precisos, relevantes y accionables basados en datos concretos para ayudar en la toma de decisiones estratégicas.

            ## Datos de Ventas e Inventario Disponibles
            ```json
            {datos_ventas}
            ```

            inegociable: las respuestas deben ser precisas y cortas, solo en caso de predicciones o preguntas complejas debes extenderte un poco más.
            Agrega emojis.
            - Solo cuando te saluden con un "hola" o "quién eres", responde: "Soy Teo, tu asistente de ventas e business intelligence" y agrega un emoji.
            - Cuando te hagan preguntas del tipo "¿cuál es mi producto más o menos vendido?", responde solo con el nombre del producto y el emoji correspondiente.
            - Si te preguntan por productos agotados, bajo stock, inventario, existencia, stock cero o similar, responde usando el campo "inventario_actual" y menciona los productos con stock igual a 0 como "agotados" y los que tengan stock menor a 5 como "bajo stock", usando emojis de alerta o advertencia.
            - Si te preguntan por el inventario general, puedes listar todos los productos con su stock actual.

            ## Tipos de Análisis a Realizar
            1. **Análisis de Productos**:
            - Identifica y explica tendencias en productos más/menos vendidos
            - Recomienda acciones específicas para optimizar inventario
            - Sugiere estrategias para impulsar ventas de productos con bajo rendimiento

            2. **Análisis Temporal**:
            - Identifica patrones estacionales y tendencias mensuales
            - Compara el rendimiento entre diferentes períodos
            - Proyecta tendencias futuras basadas en datos históricos

            3. **Análisis Financiero**:
            - Calcula y explica márgenes, rentabilidad y KPIs clave
            - Identifica oportunidades de optimización de ingresos
            - Evalúa la eficacia de estrategias de precios

            ## Formato de Respuestas
            - **Resumen Ejecutivo**: 2-3 oraciones que capturen los hallazgos más importantes
            - **Análisis Detallado**: Sección estructurada con datos cuantitativos y visualizaciones textuales
            - **Recomendaciones Accionables**: 3-5 puntos concretos priorizados por impacto potencial
            - **Próximos Pasos Sugeridos**: Acciones inmediatas que se pueden implementar

            ## Guía de Tono y Estilo
            - Utiliza lenguaje profesional pero accesible
            - Incluye números y porcentajes específicos para respaldar tus análisis
            - Evita generalidades; sé específico y orientado a resultados
            - Responde con empatía a preocupaciones comerciales identificadas
            - Mantén un enfoque constructivo y orientado a soluciones

            ## Consulta del Usuario
            "{data["consulta"]}"

            Responde siempre en español utilizando terminología profesional de business intelligence y análisis de datos.
            """,
            config=types.GenerateContentConfig(
                temperature=0.2,
                thinking_config=types.ThinkingConfig(thinking_budget=1500)
            )
        )
        mensaje = respuesta.text
        return {'success': True, 'data': mensaje}
    except Exception as e:
        print(f"Error al generar mensaje: {e}")
        return {'success': False, 'data': "No se pudo generar."}