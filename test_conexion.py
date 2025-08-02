import streamlit as st
import mysql.connector

st.subheader("Conexión a MySQL")

try:
    # Cambia estos datos por los de tu MySQL
    conexion = mysql.connector.connect(
        host="localhost",
        port=3306,
        user="root",        # tu usuario
        password="bdMl2025.",    # tu contraseña
        database="bd_amazon_ecom"  # tu base de datos
    )

    cursor = conexion.cursor()
    cursor.execute("SELECT COUNT(1) FROM DE_RAT_GEN_CAT")
    resultado = cursor.fetchone()

    st.success(f"Conectado a MySQL. La tabla DE_RAT_GEN_CAT tiene {resultado[0]} registros.")

except Exception as e:
    st.error(f"No me pude conectar a MySQL: {e}")