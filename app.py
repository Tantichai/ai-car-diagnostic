import streamlit as st
import pandas as pd  # <--- ต้องมีบรรทัดนี้เพื่อไม่ให้ NameError: pd is not defined
import os
from groq import Groq

# 1. ดึง Key จาก Environment Variable ที่ตั้งไว้ใน Render
# ตรวจสอบให้แน่ใจว่าในหน้า Render ตั้งชื่อ Key ว่า GROQ_API_KEY
api_key_from_env = os.environ.get("GROQ_API_KEY") 
client = Groq(api_key=api_key_from_env)

st.set_page_config(page_title="Car AI Diagnostic", page_icon="🚗")
st.title("🚗 AI วิเคราะห์อาการเสียรถยนต์")

@st.cache_data
def load_data():
    try:
        # อ่านไฟล์ฐานข้อมูลภาษาไทยของคุณ
        return pd.read_csv('car_data.csv')
    except Exception as e:
        st.error(f"ไม่สามารถโหลดไฟล์ car_data.csv ได้: {e}")
        return pd.DataFrame(columns=['code', 'symptom', 'fix'])

df = load_data()

# --- 2. ส่วนรับข้อมูลจากผู้ใช้ ---
st.write("อธิบายอาการเสียของรถเป็นภาษาไทย:")
user_query = st.text_input("ตัวอย่าง: เครื่องสั่นเวลาจอดนิ่งๆ หรือ มีเสียงดังที่ล้อ", key="car_input")

# --- 3. ส่วนการทำงานของปุ่มวิเคราะห์ ---
if st.button("ให้ AI วิเคราะห์อาการ"):
    if user_query:
        with st.spinner('AI กำลังวิเคราะห์ข้อมูล...'):
            # แปลงข้อมูลใน CSV เป็นข้อความเพื่อให้ AI อ่าน
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
                # ใช้โมเดลล่าสุดตามที่คุณต้องการ
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.5
                )
                
                st.divider()
                st.markdown("### 📋 ผลการวิเคราะห์")
                st.write(completion.choices[0].message.content)
            except Exception as e:
                # กรณีเกิดปัญหา ให้แสดงข้อความแจ้งเตือน
                st.error(f"เกิดข้อผิดพลาดจากระบบ AI: {e}")
                st.info("คำแนะนำ: ตรวจสอบว่าคุณได้ตั้งค่า GROQ_API_KEY ในหน้า Render เรียบร้อยแล้ว")
    else:
        st.warning("กรุณากรอกอาการเสียก่อนครับ")