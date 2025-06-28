from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

# 1. Membuat instance dari kelas FastAPI
app = FastAPI()

# 2. Membuat "path operation decorator"
@app.get("/")
def read_root():
    # 3. Fungsi yang akan dijalankan ketika endpoint diakses
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id, "description": f"Ini adalah detail untuk item {item_id}"}

@app.get("/search")
def search_items(keyword: str, short: bool = False):
    if short:
        return {"result": f"Hasil pencarian singkat untuk: '{keyword}'"}
    else:
        return {"result": f"Ini adalah hasil pencarian LENGKAP dan DETAIL untuk keyword: '{keyword}'"}
    
# Gabungan Path & Query Parameter
@app.get("/users/{user_id}/items/{item_id}")
def read_user_item(user_id: int, item_id: str, q: Optional[str] = None):
    item_data = {"item_id": item_id, "owner_id": user_id}
    if q:
        item_data.update({"query_string": q})
    return item_data

# Endpoint untuk membuat item baru menggunakan Request Body
@app.post("/items/")
def create_item(item: Item):
    return item




