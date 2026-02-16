import pandas as pd
from streamlit_gsheets import GSheetsConnection
import streamlit as st
import asyncio
import edge_tts
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import speech_recognition as sr
import os
import base64

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="DIDAPOD EDGE", page_icon="🌐", layout="centered")

def get_base64_logo(path):
    if os.path.exists(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

logo_data = get_base64_logo("logo2.png")

# --- 2. DESIGN ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #0f172a !important; }}
    div.stButton > button {{ 
        background-color: #000000 !important; 
        color: #ffffff !important; 
        border: 2px solid #ffffff !important; 
        border-radius: 12px !important; 
        font-weight: 800 !important; 
        width: 100% !important; 
        height: 50px !important;
    }}
    h1, h2, h3, label, p, span {{ color: white !important; }}
    .logo-container {{ text-align: center; margin-bottom: 20px; }}
    </style>
    """, unsafe_allow_html=True)

if logo_data:
    st.markdown(f'<div class="logo-container"><img src="data:image/png;base64,{logo_data}" width="200"></div>', unsafe_allow_html=True)

# --- 3. LOGIN & SHEETS CONNECTION ---
if "auth" not in st.session_state: 
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    with st.form("login"):
        st.markdown("### 📝 DIDAPOD EDGE ACCESS")
        email_cliente = st.text_input("📧 Your Email")
        u = st.text_input("Username", value="admin")
        p = st.text_input("Password", type="password", value="didactai2026")
        
        if st.form_submit_button("ENTER DIDAPOD"):
            if email_cliente and u == "admin" and p == "didactai2026":
                try:
                    conn = st.connection("gsheets", type=GSheetsConnection)
                    df_existente = conn.read()
                    nuevo = pd.DataFrame([{"Email": email_cliente, "Date": str(pd.Timestamp.now())}])
                    conn.update(data=pd.concat([df_existente, nuevo], ignore_index=True))
                    st.session_state["auth"] = True
                    st.rerun()
                except:
                    st.session_state["auth"] = True # Login fallback
                    st.rerun()
    st.stop()

# --- 4. EDGE-TTS ENGINE ---
async def process_voice(text, voice, file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file)

# --- 5. INTERFACE ---
st.markdown("<h1 style='text-align:center;'>🎙️ DIDAPOD EDGE (FREE)</h1>", unsafe_allow_html=True)
st.write("---")

c1, c2 = st.columns(2)
with c1:
    target_lang = st.selectbox("Language:", ["English", "Spanish", "French", "Portuguese"])
with c2:
    gender = st.selectbox("Voice Tone:", ["Male", "Female"])

up_file = st.file_uploader("Upload podcast", type=["mp3", "wav"])

# Lógica del Botón: Se activa si up_file existe
if up_file is not None:
    st.audio(up_file)
    
    # El botón ahora está claramente fuera de cualquier otra condición de visualización
    if st.button("🚀 START EDGE DUBBING"):
        try:
            with st.spinner("🤖 Processing with Edge-TTS..."):
                with open("temp.mp3", "wb") as f: 
                    f.write(up_file.getbuffer())
                
                audio = AudioSegment.from_file("temp.mp3")
                # Fragmentos de 40 segundos para evitar errores de timeout
                chunks = [audio[i:i + 40000] for i in range(0, len(audio), 40000)]
                final_audio = AudioSegment.empty()
                r = sr.Recognizer()
                
                lang_codes = {"English": "en", "Spanish": "es", "French": "fr", "Portuguese": "pt"}
                
                # Mapeo de voces de Microsoft Edge
                if gender == "Female":
                    voices = {"English": "en-US-AvaNeural", "Spanish": "es-ES-ElviraNeural", "French": "fr-FR-DeniseNeural", "Portuguese": "pt-BR-FranciscaNeural"}
                else:
                    voices = {"English": "en-US-AndrewNeural", "Spanish": "es-ES-AlvaroNeural", "French": "fr-FR-RemyNeural", "Portuguese": "pt-BR-AntonioNeural"}

                for i, chunk in enumerate(chunks):
                    chunk.export("c.wav", format="wav")
                    with sr.AudioFile("c.wav") as src:
                        try:
                            audio_data = r.record(src)
                            text = r.recognize_google(audio_data, language="es-ES")
                            trans = GoogleTranslator(source='auto', target=lang_codes[target_lang]).translate(text)
                            
                            nombre_v = f"v{i}.mp3"
                            # Ejecución asíncrona de la voz
                            asyncio.run(process_voice(trans, voices[target_lang], nombre_v))
                            
                            final_audio += AudioSegment.from_file(nombre_v)
                            os.remove(nombre_v)
                        except Exception as e:
                            continue
                
                output_path = "result_edge.mp3"
                final_audio.export(output_path, format="mp3")
                st.audio(output_path)
                
                with open(output_path, "rb") as f:
                    st.download_button("📥 DOWNLOAD", f, "didapod_edge.mp3")
                    
        except Exception as e: 
            st.error(f"Error: {e}")
else:
    st.info("💡 Please upload an audio file to enable the Dubbing button.")
