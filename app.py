import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA AYARLARI ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓", layout="centered")

# --- 2. API VE MODEL YAPILANDIRMASI ---
# Sizin verdiğiniz yeni API Key
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"
genai.configure(api_key=API_KEY)

# Sizin güçlü IBL mimariniz (Sistem Talimatı)
SYSTEM_PROMPT = """
Sen ileri düzey bir Sorgulama Temelli Öğretim (IBL) uzmanı akademisyensin. 
Görevin: Üniversite öğretim üyelerine bu yöntemi bilimsel araştırma süreçleriyle entegre ederek öğretmektir.

🔴 KRİTİK KURALLAR:
1. Asla doğrudan bilgi verme. Her aşamada soru sor ve cevap bekle.
2. Cevaplara göre öğretimi adapte et. Eksikleri düzeltmeden ilerleme.
3. Günlük hayat + akademik teori bağı kur.
4. ASLA tek yönlü anlatım yapma. Sor, bekle, analiz et, düzelt ve ilerle.

Eğitime 1. Adım olan 'STEP-BACK' (Sorgulama temelli öğretim nedir?) ile başla.
"""

# Hata Toleranslı Model Yükleyici (404 Hatalarını Aşmak İçin)
@st.cache_resource
def load_robust_model():
    # Google'ın kabul edebileceği tüm olası model varyasyonları
    variants = [
        "gemini-1.5-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest"
    ]
    for m_name in variants:
        try:
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=SYSTEM_PROMPT
            )
            # Modeli test et (boş bir deneme yap)
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except Exception:
            continue
    return None

model_engine = load_robust_model()

# --- 3. ARAYÜZ ---
st.title("🎓 IBL Akademik Mentor")
st.caption("Sorgulama Temelli Öğretim ve Bilimsel Araştırma Yöntemleri")

if model_engine is None:
    st.error("⚠️ Model Başlatılamadı.")
    st.info("Lütfen GitHub'daki 'requirements.txt' dosyasında 'google-generativeai>=0.8.0' olduğundan emin olun.")
    st.stop()

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM DÖNGÜSÜ ---
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Yanıtı Oluşturma
    with st.chat_message("assistant"):
        # Geçmişi Gemini formatına çevir (assistant -> model)
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        try:
            chat = model_engine.start_chat(history=history)
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            placeholder = st.empty()
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"API Hatası: {str(e)}")

# İlk Açılış Tetikleyicisi (Boşsa Başlat)
if not st.session_state.messages:
    try:
        initial_chat = model_engine.start_chat(history=[])
        res = initial_chat.send_message("Eğitimi 1. adımdan başlat.")
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()
    except:
        pass
