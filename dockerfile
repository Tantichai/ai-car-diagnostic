# ใช้ Python 3.9 แบบ slim เพื่อให้ขนาดเล็กและประหยัดแรมบน Render [cite: 44]
FROM python:3.9-slim

# ตั้งค่าพื้นฐานเพื่อไม่ให้เกิดไฟล์ขยะและให้แสดง Log ทันที [cite: 45, 46]
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# กำหนดโฟลเดอร์ทำงานใน Container [cite: 47]
WORKDIR /app

# ติดตั้ง dependencies ที่จำเป็นสำหรับระบบ (สำหรับโหลดโมเดลภาษาไทย)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    && rm -rf /var/lib/apt/lists/*

# คัดลอกไฟล์ requirements.txt และติดตั้ง Library [cite: 48, 49]
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์ทั้งหมด (รวมถึง app.py และ car_data.csv) เข้าไปใน Container [cite: 49]
COPY . .

# เปิด Port 8501 สำหรับ Streamlit [cite: 50]
EXPOSE 8501

# คำสั่งรันแอปพลิเคชันเมื่อ Container เริ่มทำงาน [cite: 51]
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]