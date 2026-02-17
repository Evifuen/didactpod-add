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
import tempfile

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

# --- 3. LOGIN ---
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
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 4. ENGINE ---
async def process_voice(text, voice, file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(file)

# --- 5. INTERFACE (CÓDIGO REFORZADO) ---
up_file = st.file_uploader("Upload podcast", type=["mp3", "wav"])

if up_file is not None:
    # Mostramos el audio
    st.audio(up_file)
    
    # FORZAMOS LA APARICIÓN DEL BOTÓN
    # No lo metas dentro de otros 'if' o columnas complejas
    btn_dubbing = st.button("🚀 START EDGE DUBBING", use_container_width=True)
    
    if btn_dubbing:
        try:
            with st.spinner("🤖 Procesando..."):
                # Aquí pones tu lógica de traducción
                st.write("Iniciando proceso...")
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("👋 Por favor, sube un archivo MP3 o WAV para mostrar el botón de Dubbing.")

