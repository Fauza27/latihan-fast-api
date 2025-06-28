# app/core/ml_model.py
import joblib
import numpy as np
from app.models.iris import IrisInput
from fastapi import HTTPException, status

class IrisModel:
    def __init__(self):
        self.model = None
        self.target_names = None

    def load_model(self, model_path: str = "iris_model.joblib"):
        try:
            print("Mencoba memuat model dari path:", model_path)
            self.model = joblib.load(model_path)
            self.target_names = ['setosa', 'versicolor', 'virginica']
            print("Model berhasil dimuat.")
        except FileNotFoundError:
            print(f"Error: File model tidak ditemukan di '{model_path}'")
            # Dalam aplikasi nyata, Anda mungkin ingin menghentikan aplikasi
            # atau memberikan status 'tidak sehat'. Untuk API, ini lebih sulit.
            # Kita akan set model ke None dan biarkan predict() yang handle.
            self.model = None
        except Exception as e:
            print(f"Terjadi error saat memuat model: {e}")
            self.model = None

    def predict(self, input_data: IrisInput) -> dict:
        if self.model is None:
            # Jika model gagal dimuat, lempar error 503 Service Unavailable
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Model ML tidak tersedia saat ini. Silakan hubungi administrator."
            )
        if not self.model:
            raise RuntimeError("Model belum dimuat. Panggil load_model() terlebih dahulu.")

        features = np.array([[
            input_data.sepal_length,
            input_data.sepal_width,
            input_data.petal_length,
            input_data.petal_width
        ]])

        prediction_code = self.model.predict(features)[0]
        prediction_name = self.target_names[prediction_code]

        return {
            "prediction_code": int(prediction_code),
            "prediction_name": prediction_name
        }

# Buat satu instance untuk digunakan di seluruh aplikasi
ml_model = IrisModel()