import streamlit as st
import os
from groq import Groq

# ใช้บรรทัดนี้แทนการใส่ Key ตรงๆ
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

st.set_page_config(page_title="Car AI Diagnostic", page_icon="🚗")
st.title("🚗 AI วิเคราะห์อาการเสียรถยนต์")

@st.cache_data
def load_data():
    try:
        return pd.read_csv('car_data.csv')
    except:
        return pd.DataFrame(columns=['code', 'symptom', 'fix'])

df = load_data()

# --- 2. ส่วนรับข้อมูลจากผู้ใช้ ---
st.write("อธิบายอาการเสียของรถเป็นภาษาไทย:")
user_query = st.text_input("ตัวอย่าง: เครื่องสั่นเวลาจอดนิ่งๆ หรือ มีเสียงดังที่ล้อ", key="car_input")

# --- 3. ส่วนการทำงานของปุ่มวิเคราะห์ ---
if st.button("ให้ AI วิเคราะห์อาการ"):
    if user_query:
        with st.spinner('AI กำลังวิเคราะห์ข้อมูล...'):
            csv_info = df.to_string(index=False)
            
            prompt = f"""
            คุณคือผู้เชี่ยวชาญด้านเครื่องยนต์ (Expert Mechanic)
            นี่คือฐานข้อมูลที่เรามี:
            {csv_info}
            
            ผู้ใช้ถามว่า: "{user_query}"
            
            หน้าที่ของคุณ:
            1. ตรวจสอบว่าอาการนี้ตรงกับข้อมูลในฐานข้อมูลหรือไม่
            2. ถ้าตรง ให้บอก 'รหัส' และ 'วิธีแก้' ตามฐานข้อมูล
            3. ถ้าไม่ตรง ให้ใช้องค์ความรู้ AI วิเคราะห์และแนะนำวิธีซ่อม
            4. ตอบเป็นภาษาไทย
            """
            
            try:
                # วางตรงนี้ครับ! เปลี่ยนจาก llama3-8b-8192 เป็น llama-3.3-70b-versatile
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                
                st.divider()
                st.markdown("### 📋 ผลการวิเคราะห์")
                st.write(completion.choices[0].message.content)
            except Exception as e:
                # ถ้า llama-3.3 ยังติดปัญหา ให้ใช้ตัวสำรองคือ "llama-3.1-8b-instant"
                st.error(f"เกิดข้อผิดพลาด: {e}")
    else:
        st.warning("กรุณากรอกอาการเสียก่อนครับ")