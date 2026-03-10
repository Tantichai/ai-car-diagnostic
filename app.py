import streamlit as st
import pandas as pd
from transformers import pipeline

st.set_page_config(page_title="Car AI Database", page_icon="🚗")
st.title("🚗 AI วิเคราะห์อาการจากฐานข้อมูล")

# ฟังก์ชันโหลดโมเดล AI
@st.cache_resource 
def load_ai():
    return pipeline("zero-shot-classification", model="moritzlaurer/mDeBERTa-v3-base-mnli-xnli")

# ฟังก์ชันดึงข้อมูลจาก CSV (เสมือนดึงจาก Database)
def load_data():
    return pd.read_csv('car_data.csv')

classifier = load_ai()
df = load_data()

st.write("ระบุอาการเสียที่พบ:")
user_input = st.text_input("ตัวอย่าง: เครื่องสั่นมาก")

if st.button("ค้นหาและวิเคราะห์"):
    if user_input:
        with st.spinner('กำลังค้นหาข้อมูลในระบบ...'):
            # 1. ให้ AI วิเคราะห์ว่าอาการที่พิมพ์มา ตรงกับรหัสไหนใน CSV มากที่สุด
            labels = df['symptom'].tolist()
            result = classifier(user_input, labels)
            
            # 2. ดึงข้อมูลแถวที่ AI เลือกมาแสดง
            best_match_symptom = result['labels'][0]
            matched_row = df[df['symptom'] == best_match_symptom].iloc[0]
            
            st.divider()
            st.success(f"🔍 พบข้อมูลที่ใกล้เคียงที่สุด (ความแม่นยำ: {result['scores'][0]:.2%})")
            st.write(f"**รหัส Error:** {matched_row['code']}")
            st.write(f"**สาเหตุ:** {matched_row['description']}")
            st.error(f"🛠️ **วิธีแก้ไข:** {matched_row['fix']}")
    else:
        st.warning("กรุณากรอกอาการก่อนครับ")