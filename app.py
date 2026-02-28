import streamlit as st
import os
import subprocess
import shutil
from zipfile import ZipFile

# Configuración de la página
st.set_page_config(page_title="Mi spotdl Web", page_icon="🎵")

st.title("🎵 Descargador de Playlist Personal")
st.markdown("---")

# --- SEGURIDAD ---
# Cambia "mi_clave_secreta" por la palabra que tú quieras
PASSWORD_CORRECTA = "radd" 

with st.sidebar:
    st.header("Configuración")
    pass_input = st.text_input("Introduce la contraseña:", type="password")

if pass_input == PASSWORD_CORRECTA:
    playlist_url = st.text_input("Pega la URL de Spotify (Playlist o Canción):", placeholder="https://open.spotify.com/playlist/...")
    
    if st.button("🚀 Iniciar Descarga"):
        if playlist_url:
            output_folder = "descargas_temp"
            zip_path = "mis_canciones.zip"
            
            # Limpieza previa de archivos viejos
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            os.makedirs(output_folder)

            with st.spinner("Descargando y procesando... esto puede tardar unos minutos."):
                try:
                    # Usamos 'python -m spotdl' para evitar el error de 'command not found'
                    # Añadimos --format mp3 por defecto
                    command = f'python -m spotdl download "{playlist_url}" --output "{output_folder}"'
                    
                    # Ejecutamos el comando y capturamos la salida
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    
                    if result.returncode == 0:
                        # Crear el archivo ZIP
                        archivos = os.listdir(output_folder)
                        if archivos:
                            with ZipFile(zip_path, 'w') as zipf:
                                for root, dirs, files in os.walk(output_folder):
                                    for file in files:
                                        zipf.write(os.path.join(root, file), file)
                            
                            st.success(f"✅ ¡Hecho! Se descargaron {len(archivos)} canciones.")
                            
                            # Botón de descarga
                            with open(zip_path, "rb") as f:
                                st.download_button(
                                    label="💾 Descargar mis archivos (.zip)",
                                    data=f,
                                    file_name="musica_spotify.zip",
                                    mime="application/zip"
                                )
                        else:
                            st.error("No se encontraron archivos descargados. Revisa el link.")
                    else:
                        st.error("Error al ejecutar spotdl:")
                        st.code(result.stderr)
                
                except Exception as e:
                    st.error(f"Error inesperado: {str(e)}")
        else:
            st.warning("Escribe una URL primero.")
else:
    if pass_input:
        st.error("❌ Contraseña incorrecta")
    st.info("Escribe la contraseña en el menú lateral para desbloquear.")

st.markdown("---")
st.caption("Uso personal - Desarrollado con Streamlit + spotdl")
