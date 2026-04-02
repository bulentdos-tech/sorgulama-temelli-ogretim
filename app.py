import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"

# --- 2. MODELİ "v1" KANALIYLA ZORLAYARAK BAŞLATMA ---
@st.cache_resource
def load_v1_model():
    try:
        genai.configure(api_key=API_KEY)
        
        # 404 hatasını aşmak için API sürümünü 'v1' olarak zorluyoruz
        # Bu, 'v1beta' kanalındaki kısıtlamaları devre dışı bırakır
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction="Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. Üniversite hocalarına bu yöntemi öğretiyorsun. Kural: Asla doğrudan bilgi verme, hep soru sorarak ilerlet. Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."
        )
        
        # Test çağrısı (v1 sürümü üzerinden)
        model.generate_content("test", request_options=RequestOptions(api_version="v1"))
        return model
    except Exception as e:
        return str(e)

model_engine = load_v1_model()

# --- 3. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")

if isinstance(model_engine, str):
    st.error(f"⚠️ Teknik Engel: {model_engine}")
    st.info("Eğer hala 404 alıyorsanız, tek çözüm Google AI Studio'da sol üstteki 'Create API key in NEW project' butonuna basarak yepyeni bir anahtar almaktır.")
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
        try:
            history = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            chat = model_engine.start_chat(history=history)
            # Yanıt alırken de v1 sürümünü kullanıyoruz
            response = chat.send_message(prompt, request_options=RequestOptions(api_version="v1"))
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"API Hatası: {e}")

# İlk Mesaj
if not st.session_state.messages:
    try:
        res = model_engine.generate_content("Eğitimi başlat.", request_options=RequestOptions(api_version="v1"))
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()
    except:
        pass
