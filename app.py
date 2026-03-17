import streamlit as st
from core.llm_engine import procesar_mensaje

st.set_page_config(page_title="Biótica Bot", page_icon="🌱", layout="wide")

st.title("🌱 Test del Cerebro IA - Biótica")

mensaje_prueba = st.text_input("Escribe un mensaje de prueba para el bot:", "Hola, necesito un estudio de fauna urgente para evitar una multa.")

if st.button("Probar IA"):
    with st.spinner("Pensando..."):
        # Llamamos a nuestro motor
        resultado = procesar_mensaje(mensaje_prueba)
        
        # Mostramos los resultados
        st.success("¡Respuesta recibida!")
        st.write("**Mensaje que verá el cliente:**", resultado["respuesta_bot"])
        
        # Mostramos los datos clasificados
        col1, col2 = st.columns(2)
        col1.metric("Clasificación (Servicio)", resultado["clasificacion"])
        col2.metric("Nivel de Urgencia", resultado["urgencia"])
        
        st.write("---")
        st.write("**JSON Crudo (Para la Base de Datos):**")
        st.json(resultado)