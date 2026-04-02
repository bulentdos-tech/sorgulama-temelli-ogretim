import streamlit as st
import google.generativeai as genai

# --- 1. SAYFA YAPILANDIRMASI ---
st.set_page_config(page_title="IBL Mentor", page_icon="🎓", layout="centered")

# Görsel iyileştirme (Opsiyonel)
st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. API VE MODEL AYARLARI ---
# Son aldığınız API Key
API_KEY = "AIzaSyCCiRL_OYOUdmnmTf38v0newT0VmIJqFsI"
genai.configure(api_key=API_KEY)

# Sizin mimari promptunuz (Sistem Talimatı)
SYSTEM_PROMPT = """
Sen hem ileri düzey bir prompt mühendisi hem de sorgulama temelli öğretim (Inquiry-Based Learning) alanında uzman bir akademisyensin. Aynı zamanda bilimsel araştırma yöntemleri konusunda uzmansın.
Görevin: Üniversitedeki öğretim üyelerine sorgulama temelli öğretimi derinlemesine öğretmek ve bunu bilimsel araştırma süreçleriyle entegre ederek uygulamalı şekilde kazandırmaktır.

# 🔴 GENEL KURALLAR
- Öğrenci (öğretim üyesi) pasif kalamaz. Her aşamada soru sor ve cevap bekle.
- Cevaplara göre öğretimi adapte et. Eksikleri düzeltmeden ilerleme.
- Günlük hayat + akademik teori birlikte ver. Basitten karmaşığa ilerle.
- ASLA tek yönlü anlatım yapma. Sor, bekle, analiz et, düzelt ve ilerle.

# 🧠 ÖĞRETİM MİMARİSİ
1. STEP-BACK: Sorgulama temelli öğretim nedir? Neden gereklidir? (Sor ve bekle)
2. DECOMPOSITION: Bileşenleri (hipotez, veri vb.) analiz ettir.
3. CHAIN OF THOUGHT: Senaryo yazdır.
4. TREE OF THOUGHTS: Alternatif yaklaşımlar üret.
5. PROMPT CHAINING: Ders tasarımı (Adım adım).
6. LİTERATÜR: Teori-uygulama bağı.
7. SELF-CRITIQUE: Analiz ve geliştirme.
... (Diğer adımları da bu mantıkla uygula)

Şimdi öğretime en baştan (STEP-BACK) başla.
"""

# Hata Toleranslı Model Yükleyici
@st.cache_resource
def load_ibl_model():
    # Google'ın kabul edebileceği güncel model isimleri
    variants = ["gemini-1.5-flash-002", "gemini-1.5-flash", "models/gemini-1.5-flash"]
    for name in variants:
        try:
            m = genai.GenerativeModel(model_name=name, system_instruction=SYSTEM_PROMPT)
            # Test çağrısı (Modelin yaşadığını teyit et)
            m.generate_content("hi", generation_config={"max_output_tokens": 1})
            return m
        except Exception:
            continue
    return None

model = load_ibl_model()

# --- 3. SOHBET ARAYÜZÜ ---
st.title("🎓 IBL Akademik Mentor")
st.info("Sorgulama Temelli Öğretim ve Bilimsel Araştırma Yöntemleri Eğitimi")

if model is None:
    st.error("❌ Model başlatılamadı. Lütfen API anahtarınızı veya internet bağlantınızı kontrol edin.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. ETKİLEŞİM MANTIĞI ---
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Yanıtı
    with st.chat_message("assistant"):
        # Geçmişi dönüştür
        history = []
        for m in st.session_state.messages[:-1]:
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        try:
            chat = model.start_chat(history=history)
            # Akışlı yanıt (streaming) için:
            response = chat.send_message(prompt, stream=True)
            full_res = ""
            placeholder = st.empty()
            for chunk in response:
                full_res += chunk.text
                placeholder.markdown(full_res + "▌")
            placeholder.markdown(full_res)
            
            st.session_state.messages.append({"role": "assistant", "content": full_res})
        except Exception as e:
            st.error(f"Bir hata oluştu: {str(e)}")

# --- 5. İLK AÇILIŞ TETİKLEYİCİSİ ---
if not st.session_state.messages:
    with st.chat_message("assistant"):
        try:
            initial_chat = model.start_chat(history=[])
            # Promptun içindeki talimata göre başlaması için boş bir tetikleyici
            res = initial_chat.send_message("Eğitimi başlat.")
            st.markdown(res.text)
            st.session_state.messages.append({"role": "assistant", "content": res.text})
        except Exception as e:
            st.error(f"Başlatma hatası: {e}")
