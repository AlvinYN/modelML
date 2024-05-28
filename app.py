from flask import Flask, request, jsonify
import pandas as pd
from calculations import (
    hitung_berat_badan_ideal,
    hitung_AKEi_umur,
    hitung_kebutuhan_nutrisi,
    rekomendasi_makanan_knn_all,
    dataset
)

app = Flask(__name__)

@app.route('/api/rekomendasi', methods=['POST'])
def api_rekomendasi():
    data = request.json
    Tb = data.get('tinggi_badan')
    Bb = data.get('berat_badan')
    jenis_kelamin = data.get('jenis_kelamin')
    umur = data.get('umur')
    penyakit_input = data.get('penyakit', "").split(",")
    user_allergies = data.get('alergi', "").split(",")

    if not Tb or not jenis_kelamin or not umur or not Bb or not penyakit_input or not user_allergies:
        return jsonify({"error": "Invalid input"}), 400

    # Calculate ideal body weight
    berat_badan_ideal = hitung_berat_badan_ideal(Tb)

    # Calculate basic calorie needs
    AKEi = hitung_AKEi_umur(Bb, Tb, jenis_kelamin, umur)

    # Prepare response data
    response_data = {
        "sarapan": [],
        "makan siang": [],
        "makan malam": []
    }

    # Pisahkan dataset berdasarkan Meal ID
    dataset_sarapan = dataset[dataset['Meal ID'] == 1]
    dataset_makan_siang = dataset[dataset['Meal ID'] == 2]
    dataset_makan_malam = dataset[dataset['Meal ID'] == 3]

    print("Berat Badan Ideal (Bi):", berat_badan_ideal, "kg")
    print("Angka Kebutuhan Energi Individu (AKEi) atau REE:", AKEi, "kalori/hari")

    # Menghitung dan menampilkan rekomendasi makanan untuk setiap waktu makan
    for meal_id, meal_name, dataset_mealtime in [(1, "sarapan", dataset_sarapan), (2, "makan siang", dataset_makan_siang), (3, "makan malam", dataset_makan_malam)]:
        nutrisi_dibutuhkan = hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input, jenis_kelamin)
        print(f"Nutrisi yang dibutuhkan untuk {meal_name}: {nutrisi_dibutuhkan}")
        rekomendasi = rekomendasi_makanan_knn_all(dataset_mealtime, nutrisi_dibutuhkan, user_allergies)
        
        # Tambahkan Recipe ID ke dalam response
        response_data[meal_name] = [{"Recipe ID": int(recipe_id)} for recipe_id in rekomendasi['Recipe ID']]
        print(f"Rekomendasi untuk {meal_name}: {response_data[meal_name]}")

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
