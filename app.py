import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="IBL Akademik Mentor", layout="centered")
st.title("🎓 Sorgulama Temelli Öğretim Mentoru")

# API Anahtarı Girişi (Güvenli Alan)
with st.sidebar:
    api_key = st.text_input("Gemini API Key Giriniz:", type="password")
    st.info("API anahtarını Google AI Studio'dan alabilirsiniz.")

# SİZİN PROMPTUNUZ (SİSTEM TALİMATI)
SYSTEM_PROMPT = """
Sen hem ileri düzey bir prompt mühendisi hem de sorgulama temelli öğretim (Inquiry-Based Learning) alanında uzman bir akademisyensin...
(BURAYA YUKARIDAKİ TÜM PROMPT METNİNİZİ YAPIŞTIRIN)
"""

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_PROMPT
    )

    # Chat Geçmişi Başlatma
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Mesajları Ekranda Göster
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Kullanıcı Girdisi
    if prompt := st.chat_input("Cevabınızı buraya yazın..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Yanıtı
        with st.chat_message("assistant"):
            chat = model.start_chat(history=[
                {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
else:
    st.warning("Lütfen başlamak için yan menüye API anahtarınızı girin.")
