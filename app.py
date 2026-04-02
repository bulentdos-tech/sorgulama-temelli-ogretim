import streamlit as st
import google.generativeai as genai

# --- 1. AYARLAR VE API ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓")
API_KEY = "AIzaSyCCiRL_OYOUdmnmTf38v0newT0VmIJqFsI"
genai.configure(api_key=API_KEY)

# Sizin mimari promptunuz
SYSTEM_PROMPT = """
Sen ileri düzey bir prompt mühendisi ve Sorgulama Temelli Öğretim (IBL) uzmanı bir akademisyensin. 
Görevin: Öğretim üyelerine bu yöntemi bilimsel araştırma süreçleriyle entegre ederek öğretmek.
KURAL: Asla tek yönlü anlatma. Sor, cevap bekle, analiz et ve ilerle.
Eğitime 1. Adım olan 'STEP-BACK' (Sorgulama temelli öğretim nedir?) ile başla.
"""

# --- 2. HATA TOLERANSLI MODEL YÜKLEYİCİ (HARD-FIX) ---
@st.cache_resource
def load_robust_model():
    # Google'ın kabul edebileceği tüm olası isimlendirmeler
    model_variants = [
        "gemini-1.5-flash", 
        "models/gemini-1.5-flash", 
        "gemini-1.5-flash-002",
        "gemini-1.5-flash-latest",
        "gemini-pro"
    ]
    
    last_error = ""
    for m_name in model_variants:
        try:
            # Modeli oluştur
            model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=SYSTEM_PROMPT
            )
            # Modeli gerçekten çalışıyor mu diye test et
            model.generate_content("test", generation_config={"max_output_tokens": 1})
            return model
        except Exception as e:
            last_error = str(e)
            continue
    return last_error

model_result = load_robust_model()

# --- 3. ARAYÜZ VE SOHBET ---
st.title("🎓 IBL Akademik Mentor")

# Eğer model yüklenemediyse hatayı detaylı göster
if isinstance(model_result, str):
    st.error(f"❌ Teknik Engel: {model_result}")
    st.info("Lütfen GitHub'daki 'requirements.txt' dosyasında 'google-generativeai' sürümünün en az 0.8.0 olduğundan emin olun.")
    st.stop()

model = model_result # Başarılıysa model objesidir

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş ve Yanıt
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        history = [{"role": "model" if m["role"] == "assistant" else "user", "parts": [m["content"]]} for m in st.session_state.messages[:-1]]
        try:
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Yanıt Hatası: {e}")

# Otomatik Başlatma
if not st.session_state.messages:
    try:
        res = model.generate_content("Eğitimi 1. adımdan başlat.")
        st.session_state.messages.append({"role": "assistant", "content": res.text})
        st.rerun()
    except:
        pass
