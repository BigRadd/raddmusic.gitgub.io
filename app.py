import streamlit as st
import os
import subprocess
import shutil
import sys
from zipfile import ZipFile

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi spotdl Web", page_icon="🎵", layout="centered")

# --- FUNCIÓN CRÍTICA PARA SERVIDORES NUBE ---
def inicializar_sistema():
    """Asegura que spotdl y yt-dlp estén instalados y listos."""
    try:
        import spotdl
    except ImportError:
        with st.spinner("Instalando motores de descarga en el servidor..."):
            subprocess.check_call([sys.executable, "-m", "pip", "install", "spotdl", "yt-dlp"])
            st.rerun()

inicializar_sistema()

# --- INTERFAZ ---
st.title("🎵 Descargador Personal de Playlist")
st.markdown("---")

# --- SEGURIDAD ---
# ⚠️ CAMBIA ESTO POR TU PROPIA CONTRASEÑA ⚠️
PASSWORD_CORRECTA = "mi_clave_secreta" 

with st.sidebar:
    st.header("Seguridad")
    pass_input = st.text_input("Contraseña de acceso:", type="password")
    st.info("Esta herramienta es de uso privado.")

if pass_input == PASSWORD_CORRECTA:
    st.success("Acceso concedido")
    playlist_url = st.text_input("Pega la URL de Spotify (Playlist, Álbum o Canción):", 
                                placeholder="https://open.spotify.com/playlist/...")

    if st.button("🚀 Iniciar Descarga"):
        if not playlist_url:
            st.warning("Por favor, introduce una URL válida.")
        else:
            output_folder = "downloads_temp"
            zip_path = "mi_musica.zip"

            # Limpiar descargas anteriores para no llenar el disco del servidor
            if os.path.exists(output_folder):
                shutil.rmtree(output_folder)
            if os.path.exists(zip_path):
                os.remove(zip_path)
            
            os.makedirs(output_folder)

            with st.status("Procesando descarga...", expanded=True) as status:
                st.write("Conectando con Spotify y buscando en YouTube...")
                
                # Ejecución robusta usando el ejecutable actual de Python
                comando = [
                    sys.executable, "-m", "spotdl", 
                    "download", playlist_url, 
                    "--output", output_folder,
                    "--format", "mp3"
                ]
                
                # Ejecutar y capturar logs
                process = subprocess.run(comando, capture_output=True, text=True)

                if process.returncode == 0:
                    st.write("Comprimiendo archivos...")
                    archivos = os.listdir(output_folder)
                    
                    if archivos:
                        with ZipFile(zip_path, 'w') as zipf:
                            for root, dirs, files in os.walk(output_folder):
                                for file in files:
                                    zipf.write(os.path.join(root, file), file)
                        
                        status.update(label="✅ ¡Descarga completada!", state="complete", expanded=False)
                        st.balloons()
                        
                        # Botón final de descarga al PC del usuario
                        with open(zip_path, "rb") as f:
                            st.download_button(
                                label="💾 Descargar todo en un archivo .ZIP",
                                data=f,
                                file_name="musica_descargada.zip",
                                mime="application/zip"
                            )
                    else:
                        status.update(label="❌ No se descargó nada.", state="error")
                        st.error("No se encontraron canciones. Verifica que la playlist sea pública.")
                else:
                    status.update(label="❌ Error en el proceso.", state="error")
                    st.error("Detalle del error:")
                    st.code(process.stderr)

else:
    if pass_input:
        st.error("Contraseña incorrecta")
    st.warning("Por favor, introduce la contraseña en el menú lateral para usar la herramienta.")

st.markdown("---")
st.caption("SpotDL Web UI | Basado en Python & Streamlit")
