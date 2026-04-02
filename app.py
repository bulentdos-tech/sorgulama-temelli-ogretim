import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw" # Sizin verdiğiniz anahtar

try:
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error(f"Yapılandırma Hatası: {e}")

# --- 2. MODELİ ZORLA BAŞLATMA ---
@st.cache_resource
def force_load_model():
    # Google'ın kabul ettiği tüm varyasyonlar
    models_to_try = [
        "gemini-1.5-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "gemini-pro"
    ]
    
    errors = []
    for m_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction="Sen bir IBL uzmanısın. Eğitimi 'Sorgulama temelli öğretim nedir?' sorusuyla başlat."
            )
            # Test amaçlı küçük bir veri üretimi
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except Exception as e:
            errors.append(f"{m_name}: {str(e)}")
            continue
    return errors

result = force_load_model()

if isinstance(result, list):
    st.error("❌ Hiçbir model varyasyonu başlatılamadı.")
    with st.expander("Teknik Hata Detaylarını Gör"):
        for err in result:
            st.write(err)
    st.stop()
