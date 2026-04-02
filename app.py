import streamlit as st
import google.generativeai as genai

# 1. SAYFA AYARLARI VE TASARIM
st.set_page_config(page_title="IBL Akademik Mentor", page_icon="🎓", layout="centered")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .stChatInput { border-radius: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 Sorgulama Temelli Öğretim Mentoru")
st.caption("Akademisyenler için Bilimsel Araştırma ve Sorgulama Temelli Öğretim Rehberi")

# 2. YAPILANDIRMA (Sizin API Anahtarınız ve Model Ayarları)
API_KEY = "AAIzaSyCCiRL_OYOUdmnmTf38v0newT0VmIJqFsI"
genai.configure(api_key=API_KEY)

# SİZİN ÖZEL PROMPT MİMARİNİZ
SYSTEM_PROMPT = """
Sen hem ileri düzey bir prompt mühendisi hem de sorgulama temelli öğretim (Inquiry-Based Learning) alanında uzman bir akademisyensin. Aynı zamanda bilimsel araştırma yöntemleri konusunda uzmansın.
 
Görevin: Üniversitedeki öğretim üyelerine sorgulama temelli öğretimi derinlemesine öğretmek ve bunu bilimsel araştırma süreçleriyle entegre ederek uygulamalı şekilde kazandırmaktır.
 
AMAÇ:
- Ezber değil → düşünme öğretmek
- Pasif öğrenme değil → aktif katılım sağlamak
- Bilgi vermek değil → sorgulama becerisi kazandırmak
 
# 🔴 GENEL KURALLAR
- Öğrenci (öğretim üyesi) pasif kalamaz
- Her aşamada soru sor ve cevap bekle
- Cevaplara göre öğretimi adapte et
- Eksikleri düzeltmeden ilerleme
- Günlük hayat + akademik teori birlikte ver
- Basitten karmaşığa ilerle
- Gerekirse zorlaştır / sadeleştir
 
# 🧠 ÖĞRETİM MİMARİSİ (TÜM TEKNİKLER ENTEGRE)
## 1️⃣ STEP-BACK (BÜYÜK RESİM): Sorgulama temelli öğretim nedir? Neden gereklidir? Cevap bekle.
## 2️⃣ DECOMPOSITION (YAPI TAŞLARI): Soru sorma, hipotez, veri analizi vb. süreç neden bu sırayla işler? Sor.
## 3️⃣ CHAIN OF THOUGHT: Kendi dersi için mini bir sorgulama senaryosu yazdır.
## 4️⃣ TREE OF THOUGHTS: Senaryoyu analiz et ve alternatifler üret.
## 5️⃣ PROMPT CHAINING: Konu belirle -> Soru üret -> Etkinlik tasarla (Adım adım ve düzeltmeli).
## 6️⃣ LİTERATÜR ENTEGRASYONU: Yapılandırmacılık ve teorileri dersine nasıl uygular? Sor.
## 7️⃣ SELF-CRITIQUE: Zayıf yönleri bul ve geliştir.
## 8️⃣ EXPERTS: Eğitim bilimci, öğretmen ve öğrenci gözüyle değerlendir.
## 9️⃣ SELF-CONSISTENCY: Hedef-etkinlik-ölçme uyumunu kontrol et.
## 🔟 REVERSE ENGINEERING: Başarılı bir örneği analiz ettir.
## 1️⃣1️⃣ META-PROMPTING: Bu sistemi öğretmek için öğrenciye prompt yazdır.
## 12 ADAPTİF GELİŞİM: Performansa göre zorluğu ayarla.
 
# 🔥 ALTIN KURAL
ASLA tek yönlü anlatım yapma. HER ZAMAN: sor, bekle, analiz et, düzelt ve sonra ilerle.
Şimdi öğretime başla.
"""

# --- MODEL YAPILANDIRMASI (HATA TOLERANSLI) ---
def get_model():
    # Denenecek model isimleri (Google bazen birini, bazen diğerini kabul eder)
    model_variants = ["gemini-1.5-flash", "models/gemini-1.5-flash", "gemini-1.5-flash-latest"]
    
    for m_name in model_variants:
        try:
            temp_model = genai.GenerativeModel(
                model_name=m_name,
                system_instruction=SYSTEM_PROMPT
            )
            # Küçük bir test mesajı göndererek modelin varlığını teyit et
            temp_model.generate_content("test", generation_config={"max_output_tokens": 1})
            return temp_model
        except Exception:
            continue
    return None

model = get_model()

if model is None:
    st.error("Model yüklenemedi. Lütfen API anahtarınızın 'Gemini 1.5 Flash' modeline erişimi olduğundan emin olun.")
    st.stop()
# --- MODEL YAPILANDIRMASI SONU ---

# 3. SOHBET GEÇMİŞİ YÖNETİMİ
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. ETKİLEŞİM DÖNGÜSÜ
if prompt := st.chat_input("Cevabınızı buraya yazın..."):
    # Kullanıcı mesajını kaydet ve göster
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI Yanıtı Oluşturma
    with st.chat_message("assistant"):
        # Geçmişi Gemini formatına (user/model) dönüştür
        history = []
        for m in st.session_state.messages[:-1]:
            # Gemini 'assistant' yerine 'model' rolünü bekler
            role = "model" if m["role"] == "assistant" else "user"
            history.append({"role": role, "parts": [m["content"]]})
        
        try:
            # Sohbeti başlat ve yanıt al
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt, stream=True)
            
            full_response = ""
            placeholder = st.empty()
            for chunk in response:
                full_response += chunk.text
                placeholder.markdown(full_response + "▌")
            placeholder.markdown(full_response)
            
            # Yanıtı geçmişe ekle
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Bir teknik hata oluştu: {str(e)}")
            st.info("İpucu: API anahtarınızın kısıtlamalarını veya internet bağlantınızı kontrol edin.")

# İlk açılışta AI'nın başlaması için (Eğer geçmiş boşsa)
if len(st.session_state.messages) == 0:
    with st.chat_message("assistant"):
        initial_chat = model.start_chat(history=[])
        response = initial_chat.send_message("Merhaba, öğretime başlayalım.")
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
