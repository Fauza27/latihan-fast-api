# Dockerfile

# ---- Tahap 1: Base Image ----
# Mulai dari image resmi Python. Menggunakan versi spesifik itu baik.
# "-slim" adalah varian yang lebih kecil, bagus untuk produksi.
FROM python:3.9-slim

# ---- Tahap 2: Konfigurasi Lingkungan ----
# Menetapkan direktori kerja di dalam container.
# Semua perintah selanjutnya akan dijalankan dari direktori ini.
WORKDIR /app

# ---- Tahap 3: Instalasi Dependensi ----
# Menyalin HANYA file requirements.txt terlebih dahulu.
# Ini memanfaatkan cache Docker. Jika file ini tidak berubah,
# Docker tidak akan menjalankan ulang instalasi pip pada build berikutnya.
COPY ./requirements.txt .

# Menjalankan pip untuk menginstal semua dependensi.
# --no-cache-dir mengurangi ukuran image.
RUN pip install --no-cache-dir -r requirements.txt

# ---- Tahap 4: Menyalin Kode Aplikasi ----
# Sekarang salin semua kode aplikasi kita dari folder 'app' lokal
# ke folder 'app' di dalam container (yang sekarang menjadi /app/app).
COPY ./app ./app

# Salin juga file model kita ke root direktori kerja (/app)
COPY ./iris_model.joblib .

# ---- Tahap 5: Perintah untuk Menjalankan Aplikasi ----
# Ini adalah perintah yang akan dijalankan ketika container dimulai.
# Perhatikan --host 0.0.0.0. Ini SANGAT PENTING.
# Ini memberitahu Uvicorn untuk mendengarkan koneksi dari luar container.
# Jika Anda menggunakan 127.0.0.1, Anda tidak akan bisa mengaksesnya dari luar.
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

EXPOSE 8080

CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT