# app/main.py
from fastapi import FastAPI
from app.api import prediction
from app.core.ml_model import ml_model

app = FastAPI(title="Iris Prediction API (Structured)", version="2.0.0")

@app.on_event("startup")
def startup_event():
    ml_model.load_model()

# Sertakan router dari modul lain
app.include_router(prediction.router)

@app.get("/", tags=["General"])
def read_root():
    return {"message": "Selamat datang di Iris Prediction API v2!"}