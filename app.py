import streamlit as st
from google import genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")

# API key Streamlit Secrets üzerinden alınıyor
API_KEY = st.secrets["API_KEY"]
client = genai.Client(api_key=API_KEY)

# --- 2. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")

# Mesaj geçmişi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Önceki mesajları göster
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# İlk mesaj: sistem prompt
if not st.session_state.messages:
    system_prompt = """Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin.
Üniversite hocalarına bu yöntemi öğretiyorsun. Asla direkt bilgi verme, hep soru sorarak ilerlet.
Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."""
    try:
        res = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=system_prompt
        )
        first = res.text
        st.session_state.messages.append({"role": "assistant", "content": first})
        with st.chat_message("assistant"):
            st.markdown(first)
    except Exception as e:
        st.error(f"Başlangıç mesajı alınamadı: {e}")

# Kullanıcıdan mesaj al
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # API’ye geçmiş ve yeni soruyu gönder
    history_text = "\n".join([f"{m['role']}: {m['content']}" for m in st.session_state.messages])
    try:
        answer = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=history_text
        )
        text = answer.text
        with st.chat_message("assistant"):
            st.markdown(text)
        st.session_state.messages.append({"role": "assistant", "content": text})
    except Exception as e:
        st.error(f"API Hatası: {e}")
