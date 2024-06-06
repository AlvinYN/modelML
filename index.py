from flask import Flask, request, jsonify
import pandas as pd
from ruleBased import hitung_AKEi_umur, rekomendasi_makanan, dataset

app = Flask(__name__)

@app.route('/rekomendasi', methods=['POST'])
def get_rekomendasi():
    data = request.get_json(force=True)  # force=True untuk menghindari kesalahan parsing
    if not data or 'jenis_kelamin' not in data or 'berat_badan' not in data or 'tinggi_badan' not in data or 'umur' not in data:
        return jsonify({"error": "Data tidak lengkap"}), 400

    Tb = data.get('tinggi_badan')
    Bb = data.get('berat_badan')
    jenis_kelamin = data.get('jenis_kelamin')
    umur = data.get('umur')
    penyakit_input = data.get('penyakit', "").split(",")
    alergi_input = data.get('alergi', "").split(",")

    AKEi = hitung_AKEi_umur(Bb, Tb, jenis_kelamin, umur)
    hasil_rekomendasi = rekomendasi_makanan(dataset, penyakit_input, alergi_input, AKEi, jenis_kelamin)

    # Membagi rekomendasi berdasarkan Meal ID
    grouped_recipes = {}
    for meal_id in [1, 2, 3]:  # diasumsikan 1: sarapan, 2: makan siang, 3: makan malam
        meal_name = "sarapan" if meal_id == 1 else "makan siang" if meal_id == 2 else "makan malam"
        filtered_recipes = hasil_rekomendasi[hasil_rekomendasi['Meal ID'] == meal_id][['Recipe ID']]
        grouped_recipes[meal_name] = filtered_recipes.to_dict(orient='records')
        
    return jsonify(grouped_recipes)

if __name__ == '__main__':
    app.run(debug=True)
