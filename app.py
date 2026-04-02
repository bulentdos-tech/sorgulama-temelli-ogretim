import streamlit as st

st.title("Sorgulama Temelli Öğretim Tasarım Sistemi")

# 1. Problem / Soru
question = st.text_input("Mini senaryonu yaz: Örn: Öğretmenler kaliteli etkinlik tasarlarken neye dikkat ediyor?")
if question:
    st.write(f"Sorun: {question}")

    # 2. Hipotez oluştur
    hypothesis = st.text_area("Bu soruya ilişkin hipotezini yaz:")
    if hypothesis:
        st.write(f"Hipotezin: {hypothesis}")

        # 3. Veri toplama / analiz
        data_input = st.text_area("Varsa veri veya gözlemlerini ekle:")
        if data_input:
            st.write("Analiz önerisi: Hipotezini bu verilerle test edebilirsin.")

        # 4. Yansıtma
        reflection = st.text_area("Süreci ve sonucu değerlendir:")
        if reflection:
            st.write("Teşekkürler! Yansıtman kaydedildi.")
