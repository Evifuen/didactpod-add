mport streamlit as st
import whisper
import os
import subprocess

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="DidacPod | Didacta AI", page_icon="🎙️")

# --- BRANDING ---
if os.path.exists("logo.png"):
    st.image("logo.png", width=200)
st.title("DIDACPOD")
st.markdown("Developed by **Didacta AI**")

# --- LÓGICA ---
uploaded_file = st.file_uploader("Upload MP3", type=["mp3"])

if uploaded_file:
    if st.button("🚀 START DUBBING"):
        with st.spinner("Processing..."):
            try:
                # Guardar temporalmente
                with open("input.mp3", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                # Cargar Whisper
                model = whisper.load_model("base")
                result = model.transcribe("input.mp3")
                
                st.success("Transcription complete!")
                st.write(result["text"])
                
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Make sure packages.txt with 'ffmpeg' is created in GitHub.")
