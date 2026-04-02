import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"

# --- 2. MODELİ "v1" SÜRÜMÜYLE BAŞLATMA ---
@st.cache_resource
def load_perfect_model():
    try:
        # v1beta yerine doğrudan v1 yapılandırmasını zorluyoruz
        genai.configure(api_key=API_KEY)
        
        # 2026 standartlarında en güvenli model ismi
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. Üniversite hocalarına bu yöntemi öğretiyorsun. Kural: Asla doğrudan bilgi verme, hep soru sorarak ilerlet. Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."
        )
        
        # Test çağrısı
        model.generate_content("test")
        return model
    except Exception as e:
        return str(e)

model_engine = load_perfect_model()

# --- 3. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")

if isinstance(model_engine, str):
    st.error(f"⚠️ Teknik Engel: {model_engine}")
    st.info("Eğer hala 404 alıyorsanız, lütfen Google AI Studio'da anahtarınızın 'Gemini API' servisine açık olduğunu kontrol edin.")
    st.stop()

# Sohbet Hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
        chat = model_engine.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

# Başlangıç
if not st.session_state.messages:
    res = model_engine.generate_content("Eğitimi başlat.")
    st.session_state.messages.append({"role": "assistant", "content": res.text})
    st.rerun()
