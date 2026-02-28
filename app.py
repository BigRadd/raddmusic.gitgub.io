import streamlit as st
import os
import subprocess
import shutil
from zipfile import ZipFile

st.set_page_config(page_title="Mi spotdl Web", page_icon="🎵")

st.title("🎵 Descargador de Playlist Personal")

# --- SEGURIDAD SIMPLE ---
password = st.sidebar.text_input("Contraseña de acceso", type="password")

if password == "radd": # Cambia esto por tu contraseña personal
    playlist_url = st.text_input("Pega la URL de Spotify:")
    
    if st.button("Iniciar descarga"):
        if playlist_url:
            output_folder = "descargas_temp"
            
            # Limpiar carpetas previas si existen
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            os.makedirs(output_folder)

            with st.spinner("Descargando... esto puede tardar varios minutos dependiendo del tamaño."):
                try:
                    # Ejecutamos spotdl como proceso del sistema
                    # Usamos --format mp3 para asegurar compatibilidad
                    command = f'spotdl "{playlist_url}" --output "{output_folder}"'
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # Crear un archivo ZIP con todas las canciones
                        zip_path = "playlist_descargada.zip"
                        with ZipFile(zip_path, 'w') as zipf:
                            for root, dirs, files in os.walk(output_folder):
                                for file in files:
                                    zipf.write(os.path.join(root, file), file)
                        
                        st.success("¡Descarga finalizada con éxito!")
                        
                        # Botón para que descargues el ZIP a tu PC
                        with open(zip_path, "rb") as f:
                            st.download_button(
                                label="💾 Descargar ZIP con mi música",
                                data=f,
                                file_name="mis_canciones.zip",
                                mime="application/zip"
                            )
                    else:
                        st.error(f"Error en spotdl: {result.stderr}")
                
                except Exception as e:
                    st.error(f"Ocurrió un error inesperado: {e}")
        else:
            st.warning("Por favor, introduce una URL válida.")
else:
    st.info("Introduce la contraseña en la barra lateral para usar la herramienta.")
