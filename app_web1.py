import streamlit as st
import whisper
import time
import io
import os
import httpx
from pydub import AudioSegment, effects
from deep_translator import GoogleTranslator

# --- 1. PAGE CONFIG & BRANDING ---
st.set_page_config(page_title="DidacPod by Didacta AI", page_icon="🎙️", layout="centered")

def apply_custom_styles():
    st.markdown("""
        <style>
        .stApp { background-color: #0b0e14; color: #ffffff; }
        .stButton>button {
            background: linear-gradient(90deg, #007BFF, #00c6ff);
            color: white; border: none; border-radius: 8px;
            font-weight: bold; height: 3.5em; width: 100%;
            transition: 0.3s;
        }
        .stButton>button:hover { transform: scale(1.02); box-shadow: 0px 4px 15px rgba(0,123,255,0.4); }
        .stProgress > div > div > div > div { background-color: #007BFF; }
        .sidebar .sidebar-content { background-image: linear-gradient(#2e3136,#2e3136); }
        h1, h2, h3 { font-family: 'Inter', sans-serif; text-align: center; }
        </style>
    """, unsafe_allow_html=True)

apply_custom_styles()

# --- 2. LOGO AND HEADER ---
# Nota: Reemplaza 'logo_didacta.png' con la ruta real de tu archivo de imagen
col1, col2, col3 = st.columns([1,2,1])
with col2:
    # Si tienes el archivo físico, usa: st.image("logo_didacta.png")
    st.markdown("<h3 style='margin-bottom:0;'>DIDACTA AI</h3>", unsafe_allow_html=True)
    st.markdown("<h1 style='margin-top:0; color:#007BFF;'>DIDACPOD</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; opacity: 0.8;'>Professional Hi-Fi Voice Dubbing & Cloning</p>", unsafe_allow_html=True)

st.divider()

# --- 3. SIDEBAR CONFIGURATION ---
with st.sidebar:
    st.title("Settings")
    api_key = st.text_input("ElevenLabs API Key", type="password", help="Enter your key to enable voice cloning.")
    st.divider()
    st.markdown("### How it works:")
    st.write("1. Upload your Spanish MP3.")
    st.write("2. We clone your unique voice.")
    st.write("3. AI translates and dubs into English.")
    st.write("4. Hi-Fi Mastering is applied.")

# --- 4. CORE ENGINE ---
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

def get_voice_preview(api_key, sample_audio):
    """Clones the voice and generates a small greeting for preview."""
    # Logic to add voice and return a small 3-second 'Hello' audio
    return None # Simplified for the template

# --- 5. MAIN INTERFACE ---
uploaded_file = st.file_uploader("Upload your Spanish Audio (MP3)", type=["mp3"])

if uploaded_file and api_key:
    # Preview Section
    with st.expander("🔍 Voice Preview (Optional)"):
        if st.button("Generate Voice Sample"):
            with st.spinner("Cloning for preview..."):
                time.sleep(2) # Simulation
                st.info("Voice preview successfully generated! Check the tone below.")
                # st.audio(sample_preview)

    st.divider()

    if st.button("🚀 START FULL MASTER DUBBING"):
        # Progress UI
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Step 1: Transcription
            status_text.text("📝 Transcribing original audio (Whisper AI)...")
            model = load_whisper_model()
            audio_bytes = uploaded_file.read()
            with open("temp_web.mp3", "wb") as f: f.write(audio_bytes)
            result = model.transcribe("temp_web.mp3", language="es")
            
            # Step 2: Translation
            status_text.text("🌐 Translating to English (Google Deep)...")
            translator = GoogleTranslator(source='es', target='en')
            # Intelligent splitting by phrases to avoid the 5000 character error
            sentences = result['text'].split('. ')
            
            # Step 3: Cloning & Synthesis (Simulation of the loop)
            final_audio = AudioSegment.empty()
            for i, text in enumerate(sentences):
                # Update progress
                prog = (i + 1) / len(sentences)
                progress_bar.progress(prog)
                status_text.text(f"🎙️ Dubbing phrase {i+1} of {len(sentences)}...")
                
                # Here would be your httpx.post call to ElevenLabs (Multilingual v2)
                time.sleep(0.3) # Simulation delay
                
            status_text.text("🎚️ Applying Hi-Fi Mastering & De-Esser...")
            time.sleep(1)
            
            st.success("✅ Dubbing process completed successfully!")
            st.balloons()
            
            # Final Result
            st.audio(audio_bytes) # Replace with processed audio
            st.download_button(
                label="📥 Download Mastered Dubbing",
                data=audio_bytes, # Replace with processed buffer
                file_name=f"didacpod_{uploaded_file.name}",
                mime="audio/mp3"
            )
            
        except Exception as e:
            st.error(f"An error occurred: {e}")

else:
    if not api_key:
        st.warning("Please enter your ElevenLabs API Key in the sidebar to begin.")
    if not uploaded_file:
        st.info("Waiting for an MP3 file...")

st.markdown("<br><br><p style='text-align: center; font-size: 0.8em; opacity: 0.5;'>Powered by Didacta AI Engine 2025</p>", unsafe_allow_html=True)