import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"

genai.configure(api_key=API_KEY)

# --- 2. MODEL YÜKLEME ---
@st.cache_resource
def load_model():
    try:
        # v1 API için Gemini Chat modelini başlat
        chat = genai.ChatModel(model="models/gemini-1.5")
        return chat
    except Exception as e:
        return str(e)

model = load_model()

# --- 3. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")

if isinstance(model, str):
    st.error(f"⚠️ Teknik Engel: {model}")
    st.info("Eğer hata devam ederse, Google AI Studio'da anahtarınızın yanında 'Gemini API' servisinin aktif olduğunu teyit edin.")
    st.stop()

# Sohbet hafızası
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan giriş al
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Chat geçmişini v1 API formatına dönüştür
            history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages[:-1]]
            # Mesajı gönder ve cevap al
            response = model.send_message(prompt, conversation=history)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"API Hatası: {e}")

# İlk mesaj: Eğitim başlat
if not st.session_state.messages:
    try:
        response = model.send_message(
            "Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. Üniversite hocalarına bu yöntemi öğretiyorsun. Kural: Asla doğrudan bilgi verme, hep soru sorarak ilerlet. Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."
        )
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Başlangıç mesajı alınamadı: {e}")
