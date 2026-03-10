FROM python:3.9-slim

# ตั้งค่าพื้นฐานไม่ให้เกิดไฟล์ขยะ
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# ติดตั้งเฉพาะ compiler เบื้องต้นที่จำเป็นสำหรับ Library บางตัว
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# ติดตั้ง Python Library จาก requirements.txt
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# คัดลอกไฟล์โปรเจกต์ทั้งหมด (รวมถึง car_data.csv)
COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]