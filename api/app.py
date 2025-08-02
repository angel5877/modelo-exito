# app/streamlit_app.py
import requests
import streamlit as st
import streamlit.components.v1 as components

# --- Config de página (título y layout) ---
#st.set_page_config(
#    page_title="Lanzamiento de un producto",
#    page_icon="📦",
#    layout="centered"
#)

st.markdown('<div class="app-title">Lanzamiento de un producto</div>', unsafe_allow_html=True)

st.markdown("""
    <style>
    .main {
        padding-top: 0rem !important;  /* Menos espacio arriba */
    }

    .app-title {
        font-size: 1.6rem;
        font-weight: 700;
        margin-top: 0rem;
        margin-bottom: 0.3rem;
        text-align: center;
    }

    .app-subtitle {
        color: #6b7280;
        text-align: center;
        margin-bottom: 0.8rem;
        font-size: 0.85rem;
    }

    label, .stSelectbox label, .stRadio label {
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        margin-bottom: 0.1rem !important;
    }

    .stSelectbox div[role="combobox"], .stRadio {
        margin-bottom: 0.2rem !important;
    }

    .stContainer {
        padding: 0.5rem !important;
    }

    .stButton button {
        margin-top: 0.8rem;
    }

    /* Subtítulo tipo subheader reducido */
    .form-subheader {
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
        color: #374151;
    }
    .block-container {
        padding-top: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- Cabecera e instrucciones ---
st.markdown('<div class="app-title">Lanzamiento de un producto</div>', unsafe_allow_html=True)

# Instrucciones (ahora al inicio)
st.markdown("""
> 🔍 **Instrucciones de uso:**  
> 1. Ingresa las características de un **producto nuevo** en los campos del formulario.  
> 2. Luego, presiona el botón **Evaluar éxito del producto** para saber si será **exitoso** o **no exitoso**.
""")
# --- Contenedor tipo "card" con borde ---
with st.container(border=True):
    st.markdown("""
    <div class="form-subheader">Información del producto</div>
    <hr style='margin-top: 0.2rem; margin-bottom: 0.5rem;'>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # 1. Campo "Especificaciones"
        ESPECIFICACIONES = [
            "0: Sin valor temático",
            "1: Arte y creatividad",
            "2: Desarrollo personal",
            "3: Entorno familiar",
            "4: Entorno laboral",
            "5: Entorno social",
            "6: Hogar",
            "7: Gestión emocional",
            "8: Cuidado personal",
            "9: Instituciones",
            "10: Innovación"
        ]
        ESPECIFICACIONES_MAP = {op: i for i, op in enumerate(ESPECIFICACIONES)}
        especificaciones = st.selectbox(
            "Especificaciones:",
            ESPECIFICACIONES,
            index=None,                     
            placeholder="Selecciona una opción"
        )
        codigo_especificaciones = ESPECIFICACIONES_MAP[especificaciones] if especificaciones is not None else None

        # 2. Campo "Categoría"
        CATEGORIAS = ["Fashion","Home Appliance","Electronics","Books","Fitness"]
        CATEGORIAS_MAP = {op: i for i, op in enumerate(CATEGORIAS)}

        categoria = st.selectbox(
            "Categoría:",
            CATEGORIAS,
            index=None,                     
            placeholder="Selecciona una opción"
        )
        codigo_categoria = CATEGORIAS_MAP[categoria] if categoria is not None else None

        # 3. Campo "Precio"
        PRECIOS = ["De $10 a $100","De $101 a $200","De $201 a $300","De $301 a $400","De $401 a $500"]
        PRECIOS_MAP = {op: i + 1  for i, op in enumerate(PRECIOS)}

        precio = st.selectbox(
            "Precio:",
            PRECIOS,
            index=None,                     
            placeholder="Selecciona una opción"
        )
        codigo_precio = PRECIOS_MAP[precio] if precio is not None else None

    with col2:
        # Público objetivo
        with st.container(border=True):
            st.markdown("""
            <div style="margin-top: 0.7rem;" class="form-subheader">Perfil del cliente</div>
            <hr style='margin-top: 0.2rem; margin-bottom: 0.5rem;'>
            """, unsafe_allow_html=True)

            col_gen, col_edad = st.columns(2)
            with col_gen:
                # 4. Campo "Género"
                GENEROS_MAP = {"Hombre": 0, "Mujer": 1, "Ambos": 2}
                genero = st.selectbox(
                    "Género:",
                    options=["Hombre", "Mujer", "Ambos"],
                    index=None,
                    placeholder="Selecciona"
                )
            with col_edad:
                # 5. Campo "Edad"
                EDADES = [
                    "1. Hasta 25",
                    "2. De 26 a 34",
                    "3. De 35 a 41",
                    "4. De 42 a 48",
                    "5. De 49 a 55",
                    "6. De 56 a 62",
                    "7. Más de 62"
                ]
                edad = st.selectbox(
                    "Edad:",
                    EDADES,
                    index=None,
                    placeholder="Selecciona"
                )
            codigo_genero = GENEROS_MAP[genero] if genero is not None else None

        # 5. Campo "Mes Lanzamiento"
        MESES = [
            "01. Enero",
            "02. Febrero",
            "03. Marzo",
            "04. Abril",
            "05. Mayo",
            "06. Junio",
            "07. Julio",
            "08. Agosto",
            "09. Setiembre",
            "10. Octubre",
            "11. Noviembre",
            "12. Diciembre"
        ]
        MESES_MAP = {
            "01. Enero":1,
            "02. Febrero":2,
            "03. Marzo":3,
            "04. Abril":4,
            "05. Mayo":5,
            "06. Junio":6,
            "07. Julio":7,
            "08. Agosto":8,
            "09. Setiembre":9,
            "10. Octubre":10,
            "11. Noviembre":11,
            "12. Diciembre":12
        }
        mes = st.selectbox(
            "Mes de lanzamiento:",
            MESES,
            index=None,
            placeholder="Selecciona el mes"
        )
        codigo_mes = MESES_MAP[mes] if mes is not None else None
############################################################################
# (Opcional) Guardamos en sesión para pasos siguientes
st.session_state["codigo_especificaciones"] = codigo_especificaciones
st.session_state["codigo_categoria"] = codigo_categoria
st.session_state["categoria"] = categoria
st.session_state["codigo_precio"] = codigo_precio
st.session_state["codigo_genero"] = codigo_genero
st.session_state["edad"] = edad
st.session_state["codigo_mes"] = codigo_mes
# st.success(f"Has seleccionado: **{especificaciones}** → Código asignado: **{codigo_especificaciones}**")

# Validación y mensaje
# Botón "Predecir"
if st.button("Evaluar éxito del producto"):
    datos = {
        "CodEspec": codigo_especificaciones,
        "CodCat": codigo_categoria,
        "Categoria": categoria, 
        "CodPrecio": codigo_precio,
        "CodGenero": codigo_genero,
        "Edad": edad,
        "CodMes": codigo_mes
    }

    # Considera como vacío: None, cadena vacía o el placeholder manual (si lo usas)
    faltantes = [k for k, v in datos.items() if v in (None, "", "— Selecciona —")]

    if faltantes:
        st.error(f"Faltan completar: {', '.join(faltantes)}.")
        st.stop()

    try:
        respuesta = requests.post("http://localhost:8000/predict", json=datos, timeout=10)
        if respuesta.status_code == 200:
            resultado = respuesta.json()["flag_exito"]

            if resultado == 1:
                st.success("""
            🎯 **¡Producto exitoso!**

            El modelo predice que este producto tiene un **alto potencial de éxito** en el mercado.

            🔎 Esto significa que:
            1. **Generará ventas desde su mes de lanzamiento**, lo cual es un buen indicador de aceptación inicial.
            2. **Durante los primeros 6 meses**, se estima que alcanzará al menos el **50% de las ventas** proyectadas para los primeros **2 años**.

            ✅ **¿Qué hacer ahora?**
            - Considera avanzar con el lanzamiento y planifica una campaña de marketing que aproveche este buen pronóstico.
            - Asegura el inventario inicial y valida que el canal de distribución esté listo.
                """)
            else:
                st.error("""
            ⚠️ **Producto no exitoso**

            Según el análisis del modelo, este producto **no debería ser lanzado en este momento**.

            🔍 ¿Por qué?
            1. Se predice que **no tendrá ventas significativas en el mes de lanzamiento**.
            2. Además, **en los primeros 6 meses** no alcanzaría un volumen relevante de ventas para justificar su producción o distribución.

            ❗ **Recomendaciones:**
            - Revisa las características del producto y considera hacer mejoras en el diseño, precio o público objetivo.
            - Evalúa lanzar el producto en otro **mes más favorable**.
            - Realiza pruebas de mercado a pequeña escala antes de invertir en un lanzamiento masivo.
                """)
        else:
            st.error("No se pudo terminar la evaluación.")

        # 👉 Scroll automático al ancla 'result'
        components.html("""
            <script>
                setTimeout(function() {
                    var element = document.getElementById("result");
                    if (element) {
                        element.scrollIntoView({ behavior: "smooth", block: "start" });
                    }
                }, 300);
            </script>
        """, height=0)

    except Exception as e:
        st.error(f"Error de conexión: {e}")

    #st.success("¡Todo listo! Estos son los valores seleccionados:")