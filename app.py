import streamlit as st

# Sayfa Yapılandırması
st.set_page_config(page_title="IBL Tasarım Sistemi", page_icon="🎓")

st.title("🚀 Sorgulama Temelli Öğretim Tasarım Sistemi")
st.info("Sorgulama temelli öğrenme (Inquiry-Based Learning) adımlarını takip ederek tasarımını oluştur.")

# --- 1. ADIM: PROBLEM / SORU ---
st.header("1. Problem / Soru")
question = st.text_input(
    "Mini senaryonu yaz:", 
    placeholder="Örn: Öğretmenler kaliteli etkinlik tasarlarken neye dikkat ediyor?"
)

if question:
    st.success(f"**Odak Sorun:** {question}")
    
    # --- 2. ADIM: HİPOTEZ ---
    st.divider()
    st.header("2. Hipotez Oluştur")
    hypothesis = st.text_area("Bu soruya ilişkin hipotezini yaz:", placeholder="Tahminimce...")

    if hypothesis:
        # --- 3. ADIM: VERİ TOPLAMA ---
        st.divider()
        st.header("3. Veri Toplama ve Analiz")
        data_input = st.text_area("Varsa veri veya gözlemlerini ekle:", placeholder="Gözlemlerim şunlar...")
        
        if data_input:
            st.info("💡 **Analiz Önerisi:** Yazdığın gözlemler, hipotezini destekliyor mu? Çelişen noktaları belirle.")

            # --- 4. ADIM: YANSITMA ---
            st.divider()
            st.header("4. Yansıtma ve Değerlendirme")
            reflection = st.text_area("Süreci ve sonucu değerlendir:", placeholder="Bu süreçten ne öğrendin?")
            
            if reflection:
                st.balloons()
                st.success("✅ Tasarım sürecin tamamlandı ve yansıtman kaydedildi!")
                
                # Özet Gösterimi
                with st.expander("Tasarım Özeti"):
                    st.write(f"**Soru:** {question}")
                    st.write(f"**Hipotez:** {hypothesis}")
                    st.write(f"**Veriler:** {data_input}")
                    st.write(f"**Yansıtma:** {reflection}")
else:
    st.warning("Devam etmek için lütfen bir soru yazarak başlayın.")
GitHub ve Streamlit İçin Son Kontrol Listesi:
requirements.txt: İçinde sadece streamlit ve pandas==2.1.0 olduğundan emin ol. (Dosya uzantısının .txt olduğundan ve küçük harfle yazıldığından emin ol).

Dosya İsimleri: GitHub'daki ana dosyanın adının tam olarak app.py olduğundan emin ol.

Streamlit Cloud: share.streamlit.io adresine gidip sorgulama-temelli-ogretim deponu bağladığında sağdaki "Logs" kısmını izle. Eğer kırmızı bir yazı çıkarsa oradaki hatayı kopyalayıp bana gönder.

Her şey yolunda giderse, birkaç dakika içinde "Your app is live" yazısını göreceksin! Uygulaman hazır olduğunda linkini denemek için sabırsızlanıyorum. Başka bir adımda takıldın mı?
