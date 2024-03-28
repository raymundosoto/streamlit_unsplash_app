import streamlit as st
import time
import requests
import configparser
import random

# Definir funciones de descarga de imágenes y búsqueda en la API de Unsplash
def download_image(url, name='image.jpg'):
    """Descarga una imagen desde una URL dada y la guarda con el nombre especificado."""
    try:
        res = requests.get(url, allow_redirects=True)
        with open(name, 'wb') as img:
            img.write(res.content)
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar la imagen: {e}")
        return False

def unsplash_api_search(query):
    """Busca una imagen en Unsplash según el query dado y devuelve la URL de una imagen aleatoria encontrada."""
    config = configparser.ConfigParser()
    config.read('key.ini')
    clave = config['key_id']['client_id']
    
    api_url = 'https://api.unsplash.com/search/photos'
    params = {'query': query, 'client_id': clave}

    try:
        res = requests.get(api_url, params=params)
        data = res.json()
        if not data.get('total'):
            return None
        # Elegir una imagen aleatoria de los resultados
        random_index = random.randint(0, len(data['results']) - 1)
        return data['results'][random_index]['urls']['raw']
    except requests.exceptions.RequestException as e:
        print(f"Error al realizar la búsqueda en la API: {e}")
        return None

# Interfaz de usuario con Streamlit
st.title("App Unsplash")
st.subheader("Esta app muestra imágenes obtenidas de Unsplash.com")
st.subheader("App creada por Raymundo S")

# Botón para obtener imágenes nuevas
if st.button("Obtener imágenes nuevas"):
    categories = ["Estrellas","Astronomía", "Animals", "Nature", "Calles", "Amor", "Comida"]
    st.text("Descargando imágenes...")  # Mostrar mensaje de descarga inicial

    for category in categories:
        st.text(f"Descargando imagen de la categoría '{category}'...")
        results_url = unsplash_api_search(category)
        if not results_url:
            st.write(f'Error al descargar imagen para la categoría: {category}')
        else:
            img_name = f"{category.replace(' ', '_')}.jpg"
            if download_image(results_url, img_name):
                pass
                #st.image(img_name, caption=f'Imagen de la categoría "{category}"')
            else:
                st.write(f'Error al descargar imagen para la categoría: {category}')

    st.text("Descarga completada")  # Mostrar mensaje de descarga completada

# Mostrar pestañas con imágenes estáticas
Estrellas, Astronomia, Animales, Naturaleza, Calles, Amor, Comida = st.tabs(["Estrellas","Astronomía", "Animales", "Naturaleza", "Calles", "Amor", "Comida"])
with Estrellas:
    st.image("Estrellas.jpg", caption="Imágenes de estrellas")

with Astronomia:
    st.image("Astronomía.jpg", caption="Astronomía")

with Animales:
    st.image("Animals.jpg", caption="Animales")

with Naturaleza:
    st.image("Nature.jpg", caption="Naturaleza")

with Calles:
    st.image("Calles.jpg", caption="Fotografía Callejera")

with Amor:
    st.image("Amor.jpg", caption="Amor")

with Comida:
    st.image("Comida.jpg", caption="Comida")
