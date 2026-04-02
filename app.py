import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")

# YENİ ANAHTARI BURAYA YAPIŞTIRIN
API_KEY = "AIzaSyDn9FccFtmjwWBtcHBz4SGnFa1h2a5PTwo"

genai.configure(api_key=API_KEY)

SYSTEM_PROMPT = """
Sen ileri düzey bir Sorgulama Temelli Öğretim (IBL) uzmanı akademisyensin. 
Görevin: Öğretim üyelerine bu yöntemi bilimsel araştırma süreçleriyle öğreterek kazandırmaktır.
KURAL: Asla tek yönlü anlatma. Sor, cevap bekle, analiz et ve ilerle.
Eğitime 1. Adım olan 'STEP-BACK' ile başla.
"""

# --- 2. MODELİ YÜKLEME ---
@st.cache_resource
def load_model():
    try:
        # En güncel kararlı sürüm
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        # Basit bir test
        model.generate_content("test", generation_config={"max_output_tokens": 1})
        return model
    except Exception as e:
        return str(e)

model_result = load_model()

# --- 3. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")

if isinstance(model_result, str):
    st.error(f"⚠️ API Hatası: {model_result}")
    st.info("Eğer 'expired' hatası devam ediyorsa, lütfen yeni oluşturduğunuz anahtarı koda doğru yapıştırdığınızdan emin olun.")
    st.stop()

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
        chat = model_result.start_chat(history=history)
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})

if not st.session_state.messages:
    initial_res = model_result.generate_content("Eğitimi başlat.")
    st.session_state.messages.append({"role": "assistant", "content": initial_res.text})
    st.rerun()
