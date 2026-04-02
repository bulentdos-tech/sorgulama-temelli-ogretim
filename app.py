import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyBP859Oq1Io1Tcrlb1NyN3_KlQonjkW5hw"

# --- 2. MODELİ ZORLAYARAK BAŞLATMA ---
@st.cache_resource
def load_robust_model():
    genai.configure(api_key=API_KEY)
    # 2026'da en stabil çalışan model isimleri
    model_names = [
        "gemini-1.5-flash", 
        "models/gemini-1.5-flash", 
        "gemini-1.5-flash-latest"
    ]
    
    errors = []
    for m in model_names:
        try:
            model = genai.GenerativeModel(
                model_name=m,
                system_instruction="Sen Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. Üniversite hocalarına bu yöntemi öğretiyorsun. Kural: Asla doğrudan bilgi verme, hep soru sorarak ilerlet. Eğitime 'Sorgulama temelli öğretim nedir?' diyerek başla."
            )
            # Test çağrısı (Çalışıp çalışmadığını kontrol et)
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except Exception as e:
            errors.append(f"{m}: {str(e)}")
            continue
    return errors

model_result = load_robust_model()

# --- 3. ARAYÜZ VE HATA YÖNETİMİ ---
st.title("🎓 IBL Akademik Mentor")

if isinstance(model_result, list):
    st.error("❌ Model Başlatılamadı.")
    with st.expander("Teknik Hata Detaylarını İncele"):
        for err in model_result:
            st.write(err)
    st.info("İpucu: Eğer 'API_KEY_INVALID' hatası alıyorsanız, Google AI Studio'da yepyeni bir 'Project' oluşturup yeni anahtar almanız gerekir.")
    st.stop()

# --- 4. SOHBET DÖNGÜSÜ ---
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

# İlk mesaj tetikleyici
if not st.session_state.messages:
    try:
        res = model_result.generate_content("Eğitimi başlat.")
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()
    except:
        pass
