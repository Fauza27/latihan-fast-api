# app/api/prediction.py
from fastapi import APIRouter, Depends
from app.models.iris import IrisInput, PredictionOut
from app.core.ml_model import ml_model

router = APIRouter()

@router.post("/predict", response_model=PredictionOut, tags=["Predictions"])
def predict_iris(input_data: IrisInput):
    """
    Endpoint untuk memprediksi tipe bunga Iris.
    """
    prediction_result = ml_model.predict(input_data)
    return prediction_result