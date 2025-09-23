import streamlit as st
from textblob import TextBlob

# Título de la app
st.title("Análisis de Sentimientos Textuales")

# Escribir instrucción
st.write("Escribe la frase para analizar su sentimiento:")

# Ingreso de texto
texto = st.text_area("Ingrese el texto aquí:")

if st.button("Analizar"):
    if texto:
        # Analizar el sentimiento utilizando TextBlob
        analizer = TextBlob(texto)
        polaridad = analizer.sentiment.polarity
        
        # Ajustar umbrales para el análisis de sentimientos
        if polaridad > 0.1:  # Sentimiento Positivo
            sentimiento = "Positivo"
            st.success(f"Sentimiento: {sentimiento}")
        elif polaridad < -0.1:  # Sentimiento Negativo
            sentimiento = "Negativo"
            st.error(f"Sentimiento: {sentimiento}")
        else:  # Sentimiento Neutral
            sentimiento = "Neutral"
            st.warning(f"Sentimiento: {sentimiento}")

        # Mostrar la polaridad de la frase
        st.write(f"Polaridad: {polaridad}")
