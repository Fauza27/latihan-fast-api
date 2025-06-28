# main.py

from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from typing import List

# --- Langkah 1: Definisikan Pydantic Model untuk Input Prediksi ---
# Model ini harus mencerminkan fitur yang dibutuhkan oleh model ML kita.
# Fitur: sepal_length, sepal_width, petal_length, petal_width
class IrisInput(BaseModel):
    sepal_length: float
    sepal_width: float
    petal_length: float
    petal_width: float

# Definisikan juga model untuk output prediksi agar lebih terstruktur
class PredictionOut(BaseModel):
    prediction_code: int
    prediction_name: str

# --- Langkah 2: Inisialisasi Aplikasi FastAPI & Tempat Penyimpanan Model ---
app = FastAPI(title="Iris Prediction API", version="1.0.0")

# Kita gunakan dictionary untuk menyimpan model agar mudah diakses.
# Ini akan diisi saat startup.
models = {}

# --- Langkah 3: Definisikan Startup Event ---
# Fungsi ini akan dijalankan HANYA SEKALI saat aplikasi dimulai.
@app.on_event("startup")
def load_model():
    print("Memuat model ML...")
    # Muat model dari file dan simpan di dictionary `models`
    models["iris_model"] = joblib.load("iris_model.joblib")
    # Siapkan juga nama kelas target
    models["iris_target_names"] = ['setosa', 'versicolor', 'virginica']
    print("Model berhasil dimuat.")
    print(f"Model yang tersedia: {list(models.keys())}")


# --- Langkah 4: Buat Endpoint untuk Prediksi ---
@app.post("/predict", response_model=PredictionOut, tags=["Predictions"])
def predict_iris(input_data: IrisInput):
    """
    Endpoint untuk memprediksi tipe bunga Iris.

    - **input_data**: Data fitur bunga Iris dalam format JSON.
    - **Returns**: Prediksi tipe bunga (kode dan nama).
    """
    # 1. Konversi data input Pydantic menjadi array NumPy
    # Model Scikit-learn mengharapkan input 2D, jadi kita gunakan [[...]]
    features = np.array([[
        input_data.sepal_length,
        input_data.sepal_width,
        input_data.petal_length,
        input_data.petal_width
    ]])

    # 2. Lakukan prediksi menggunakan model yang sudah dimuat
    model = models["iris_model"]
    prediction_code = model.predict(features)[0] # Hasilnya array, ambil elemen pertama

    # 3. Ambil nama prediksi dari kode yang dihasilkan
    target_names = models["iris_target_names"]
    prediction_name = target_names[prediction_code]

    # 4. Kembalikan hasil dalam format Pydantic 'PredictionOut'
    return {
        "prediction_code": int(prediction_code), # pastikan tipenya int
        "prediction_name": prediction_name
    }

# Endpoint dasar untuk memeriksa apakah API berjalan
@app.get("/", tags=["General"])
def read_root():
    return {"message": "Selamat datang di Iris Prediction API!"}