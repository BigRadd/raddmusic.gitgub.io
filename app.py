import streamlit as st
import os
import yt_dlp
import shutil
from zipfile import ZipFile

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Media Downloader Pro", page_icon="📥")
st.title("📥 Multi-Source Downloader")
st.markdown("Descarga desde **YouTube, YT Music, Spotify (vía YT)** y más.")

# --- SEGURIDAD ---
PASSWORD_CORRECTA = "radd" # <--- CAMBIA ESTO

with st.sidebar:
    st.header("Seguridad")
    pass_input = st.text_input("Contraseña:", type="password")

if pass_input == PASSWORD_CORRECTA:
    url = st.text_input("Pega el enlace (Playlist o Video):")
    formato = st.selectbox("Formato de salida:", ["mp3", "m4a", "wav"])
    
    if st.button("🚀 Iniciar Procesamiento"):
        if not url:
            st.warning("Por favor, pega una URL válida.")
        else:
            download_path = "downloads"
            zip_name = "descarga_total.zip"
            
            # Limpieza
            if os.path.exists(download_path): shutil.rmtree(download_path)
            if os.path.exists(zip_name): os.remove(zip_name)
            os.makedirs(download_path)

            with st.status("Analizando y descargando...", expanded=True) as status:
                # Configuración de yt-dlp
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f'{download_path}/%(title)s.%(ext)s',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': formato,
                        'preferredquality': '192',
                    }],
                    'noplaylist': False, # Permitir playlists
                }

                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        st.write("📥 Descargando archivos al servidor...")
                        ydl.download([url])
                    
                    # Comprimir resultados
                    st.write("📦 Creando paquete ZIP...")
                    archivos = os.listdir(download_path)
                    if archivos:
                        with ZipFile(zip_name, 'w') as zipf:
                            for root, dirs, files in os.walk(download_path):
                                for file in files:
                                    zipf.write(os.path.join(root, file), file)
                        
                        status.update(label="✅ ¡Todo listo!", state="complete")
                        st.balloons()
                        
                        with open(zip_name, "rb") as f:
                            st.download_button(
                                label=f"💾 Descargar {len(archivos)} archivos (.zip)",
                                data=f,
                                file_name="mis_descargas.zip",
                                mime="application/zip"
                            )
                    else:
                        st.error("No se descargó ningún archivo. Verifica el link.")
                        
                except Exception as e:
                    status.update(label="❌ Error crítico", state="error")
                    st.error(f"Detalles: {str(e)}")
else:
    st.info("Introduce la contraseña para desbloquear la herramienta.")
