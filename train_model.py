# train_model.py

from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
import joblib

print("Memulai proses training model...")

# 1. Memuat dataset Iris
iris = load_iris()
X, y = iris.data, iris.target

# Nama fitur dan nama target untuk referensi
# Fitur: sepal length, sepal width, petal length, petal width
# Target: 0 (setosa), 1 (versicolor), 2 (virginica)

# 2. Membuat dan melatih model
# Kita menggunakan Logistic Regression sebagai contoh
model = LogisticRegression(max_iter=200)
model.fit(X, y)

print("Model berhasil dilatih.")

# 3. Menyimpan model ke dalam file
# Nama file model kita adalah 'iris_model.joblib'
model_filename = "iris_model.joblib"
joblib.dump(model, model_filename)

print(f"Model telah disimpan ke file: {model_filename}")

# Contoh prediksi untuk memastikan model bekerja
# Fitur: [sepal_length, sepal_width, petal_length, petal_width]
contoh_data = [[5.1, 3.5, 1.4, 0.2]] # Contoh data untuk bunga Setosa
prediksi = model.predict(contoh_data)
nama_prediksi = iris.target_names[prediksi[0]]

print(f"Contoh prediksi untuk data {contoh_data}: kelas {prediksi[0]} ({nama_prediksi})")