import streamlit as st
import google.generativeai as genai

# 1. AYARLAR
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
st.title("🎓 Sorgulama Temelli Öğretim Mentoru")

# Sizin verdiğiniz API Key
API_KEY = "AIzaSyCCiRL_OYOUdmnmTf38v0newT0VmIJqFsI"

# 2. MODEL YAPILANDIRMASI
try:
    genai.configure(api_key=API_KEY)
    # En güncel ve en geniş kapsamlı model ismini kullanıyoruz
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction="Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. Üniversite hocalarına bu yöntemi öğretiyorsun. Kural: Asla doğrudan bilgi verme, hep soru sorarak ilerlet. Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."
    )
except Exception as e:
    st.error(f"Bağlantı Hatası: {e}")

# 3. SOHBET HAFIZASI
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekrana yazdır
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ETKİLEŞİM
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Geçmişi Gemini'nin istediği 'user' ve 'model' rollerine çeviriyoruz
            history = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"API Hatası: {e}")
            st.info("Hata devam ediyorsa Google AI Studio'dan 'Create API key in NEW project' diyerek yeni bir anahtar almanız gerekebilir.")

# İlk Mesaj (Eğer sohbet boşsa)
if not st.session_state.messages:
    try:
        res = model.generate_content("Eğitimi başlat.")
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()
    except:
        pass
