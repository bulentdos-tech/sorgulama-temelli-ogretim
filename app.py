import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA VE API YAPILANDIRMASI ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓", layout="centered")

# Sizin verdiğiniz güncel API Key
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"
genai.configure(api_key=API_KEY)

# --- 2. IBL MANTIĞI VE MODEL YÜKLEME ---
@st.cache_resource
def load_ibl_model():
    try:
        # Sistem talimatını burada veriyoruz, böylece model karakterden çıkmaz
        instruction = (
            "Sen ileri düzey bir Sorgulama Temelli Öğretim (IBL) uzmanı akademisyensin. "
            "Görevin: Üniversite hocalarına bu yöntemi öğretmek. "
            "KRİTİK KURAL: Asla doğrudan bilgi verme. Her aşamada soru sor ve gelen cevaba göre "
            "yeni bir soruyla derinleş. Eğitime 'Sorgulama temelli öğretim nedir?' sorusuyla başla."
        )
        
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=instruction
        )
        return model
    except Exception as e:
        return str(e)

model_engine = load_ibl_model()

# --- 3. SOHBET VE HAFIZA YÖNETİMİ ---
# Streamlit her etkileşimde sayfayı yenilediği için hafızayı session_state'de tutuyoruz
if "messages" not in st.session_state:
    st.session_state.messages = []

if "chat_session" not in st.session_state:
    # Gemini'nin kendi geçmiş yönetimini başlatıyoruz
    st.session_state.chat_session = model_engine.start_chat(history=[])

# --- 4. ARAYÜZ ÇİZİMİ ---
st.title("🎓 IBL Akademik Mentor")
st.caption("Sorgulama Temelli Öğretim ve Bilimsel Araştırma Yöntemleri")

# Hata kontrolü
if isinstance(model_engine, str):
    st.error(f"Model başlatılamadı: {model_engine}")
    st.stop()

# Önceki mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 5. İLK MESAJ TETİKLEME (Boşsa Başlat) ---
if not st.session_state.messages:
    try:
        # Modeli ilk kez uyandırmak için "Merhaba" diyoruz, o sistem talimatıyla cevap verecek
        initial_response = st.session_state.chat_session.send_message("Eğitimi başlat.")
        st.session_state.messages.append({"role": "assistant", "content": initial_response.text})
        with st.chat_message("assistant"):
            st.markdown(initial_response.text)
        st.rerun() # Ekranın güncellenmesi için şart
    except Exception as e:
        st.error(f"Bağlantı hatası: {e}")

# --- 6. KULLANICI ETKİLEŞİMİ ---
if prompt := st.chat_input("Cevabınızı veya sorunuzu buraya yazın..."):
    # 1. Kullanıcı mesajını ekle ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 2. AI yanıtını oluştur ve göster
    with st.chat_message("assistant"):
        try:
            # Chat session geçmişi otomatik hatırlar
            response = st.session_state.chat_session.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
