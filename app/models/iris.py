# app/models/iris.py
from pydantic import BaseModel, Field

class IrisInput(BaseModel):
    sepal_length: float = Field(..., gt=0, description="Panjang kelopak dalam cm, harus lebih dari 0")
    sepal_width: float = Field(..., gt=0, description="Lebar kelopak dalam cm, harus lebih dari 0")
    petal_length: float = Field(..., gt=0, description="Panjang mahkota dalam cm, harus lebih dari 0")
    petal_width: float = Field(..., gt=0, description="Lebar mahkota dalam cm, harus lebih dari 0")

"""
lt: less than
ge: greater than or equal to
le: less than or equal to
min_length, max_length: untuk string
regex: untuk mencocokkan pola string

from pydantic import Field: Kita perlu mengimpor Field.
= Field(...): Sebagai ganti nilai default, kita gunakan Field.
(...) (tiga titik, disebut Ellipsis): Ini memberitahu Pydantic bahwa field ini wajib diisi.
gt=0: Ini adalah aturan validasi. gt berarti greater than. Sekarang, sepal_length tidak hanya harus float, tapi juga harus bernilai lebih besar dari 0.
description="...": Kita bisa menambahkan deskripsi per-field yang akan muncul di dokumentasi /docs.
"""

class PredictionOut(BaseModel):
    prediction_code: int
    prediction_name: str