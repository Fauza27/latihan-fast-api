# tests/test_prediction_api.py

from fastapi.testclient import TestClient
from app.main import app  # Impor objek 'app' FastAPI kita
from app.core.ml_model import ml_model

ml_model.load_model()

# Buat instance TestClient
# Ini adalah "browser" atau "klien" palsu kita untuk menguji API
client = TestClient(app)


def test_read_root():
    """
    Tes untuk endpoint root (/).
    Harus mengembalikan status code 200 dan pesan yang benar.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Selamat datang di Iris Prediction API v2!"}


def test_predict_success_setosa():
    """
    Tes untuk endpoint /predict dengan data yang valid untuk kelas 'setosa'.
    """
    # Siapkan payload yang valid
    valid_payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    
    # Kirim request POST ke endpoint /predict
    response = client.post("/predict", json=valid_payload)
    
    # Periksa hasilnya
    assert response.status_code == 200
    data = response.json()
    assert data["prediction_name"] == "setosa"
    assert data["prediction_code"] == 0


def test_predict_validation_error():
    """
    Tes untuk endpoint /predict dengan data yang tidak valid.
    Contoh: nilai negatif, yang seharusnya gagal validasi Pydantic (gt=0).
    """
    # Siapkan payload yang tidak valid
    invalid_payload = {
        "sepal_length": -5.1, # Nilai ini tidak valid
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2
    }
    
    response = client.post("/predict", json=invalid_payload)
    
    # Kita harapkan error 422 Unprocessable Entity
    assert response.status_code == 422
    
    # (Opsional tapi sangat baik) Periksa isi pesan error
    data = response.json()
    assert "detail" in data
    assert data["detail"][0]["msg"] == "Input should be greater than 0"
    assert data["detail"][0]["loc"] == ["body", "sepal_length"]


def test_missing_field_error():
    """
    Tes untuk endpoint /predict dengan payload yang field-nya kurang.
    """
    incomplete_payload = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        # petal_length dan petal_width hilang
    }
    
    response = client.post("/predict", json=incomplete_payload)
    
    assert response.status_code == 422
    data = response.json()
    # Pydantic akan melaporkan field pertama yang hilang
    assert data["detail"][0]["msg"] == "Field required"
    assert data["detail"][0]["loc"] == ["body", "petal_length"]