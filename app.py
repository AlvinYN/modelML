from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector  # Pastikan ini diimpor
from calculations import (
    hitung_berat_badan_ideal,
    hitung_AKEi_umur,
    hitung_kebutuhan_nutrisi,
    rekomendasi_makanan_knn_all,
    dataset
)

app = Flask(__name__)

# def get_mysql_connection():
#     return mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="Alvinyn0506*",
#         database="backend_verif"
#     )

# def get_user_details(user_id):
#     # connection = get_mysql_connection()
#     # cursor = connection.cursor(dictionary=True)
#     query = "SELECT * FROM UserDetail WHERE user_id = %s"
#     cursor.execute(query, (user_id,))
#     user_details = cursor.fetchone()
#     cursor.close()
#     connection.close()
#     return user_details

def prepare_response_data():
    return {
        "sarapan": [],
        "makan siang": [],
        "makan malam": []
    }

def get_mealtime_dataset(meal_id):
    return dataset[dataset['Meal ID'] == meal_id]

@app.route('/api/rekomendasi', methods=['POST'])
# def api_rekomendasi():
#     data = request.json
    # user_id = data.get('user_id')
    
    # # Ambil data pengguna dari database
    # user_details = get_user_details(user_id)
    # if not user_details:
    #     return jsonify({"error": "User not found"}), 404

    # # Ambil data dari detail pengguna
    # Tb = user_details['height']
    # Bb = user_details['weight']
    # jenis_kelamin = user_details['gender']
    # umur = user_details['age']
    # penyakit_input = user_details['disease'].split(",")
    # user_allergies = user_details['allergen'].split(",")
    
def api_rekomendasi():
    data = request.json
    Tb = data.get('tinggi_badan')
    Bb = data.get('berat_badan')
    jenis_kelamin = data.get('jenis_kelamin')
    umur = data.get('umur')
    penyakit_input = data.get('penyakit', "").split(",")
    user_allergies = data.get('alergi', "").split(",")

    # Hitung berat badan ideal dan AKEi
    berat_badan_ideal = hitung_berat_badan_ideal(Tb)
    AKEi = hitung_AKEi_umur(Bb, Tb, jenis_kelamin, umur)

    # Persiapkan data untuk respon
    response_data = prepare_response_data()

    print(f"Berat Badan Ideal (Bi): {berat_badan_ideal} kg")
    print(f"Angka Kebutuhan Energi Individu (AKEi) atau REE: {AKEi} kalori/hari")
    
    # Loop untuk setiap waktu makan
    for meal_id, meal_name in [(1, "sarapan"), (2, "makan siang"), (3, "makan malam")]:
        dataset_mealtime = get_mealtime_dataset(meal_id)
        nutrisi_dibutuhkan = hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input, jenis_kelamin)
        
        print(f"Nutrisi yang dibutuhkan untuk {meal_name}: {nutrisi_dibutuhkan}")
        
        rekomendasi = rekomendasi_makanan_knn_all(dataset_mealtime, nutrisi_dibutuhkan, user_allergies, penyakit_input)
        response_data[meal_name] = [{"Recipe ID": int(recipe_id)} for recipe_id in rekomendasi['Recipe ID']]
        
        print(f"Rekomendasi untuk {meal_name}: {response_data[meal_name]}")

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
