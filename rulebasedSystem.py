import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler

# Load dataset
dataset_path = "newestUpdate_ConstrainsRecipe.csv"
dataset = pd.read_csv(dataset_path)

# Function to calculate ideal body weight
def hitung_berat_badan_ideal(Tb):
    Bi = (Tb - 100) - (0.1 * (Tb - 100))
    return Bi

# Function to calculate basic calorie needs
def hitung_AKEi_umur(Bb, Tb, jenis_kelamin, umur):
    if jenis_kelamin.lower() == "laki-laki":
        AKEi = (10 * Bb) + (6.25 * Tb) - (5 * umur) + 5
    elif jenis_kelamin.lower() == "perempuan":
        AKEi = (10 * Bb) + (6.25 * Tb) - (5 * umur) - 161
    else:
        raise ValueError("Jenis kelamin tidak valid")
    return AKEi

# Function to calculate the nutritional needs factor based on mealtime
def hitung_kebutuhan_faktor(meal_id):
    faktor_map = {1: 0.25, 2: 0.40, 3: 0.35}
    return faktor_map[meal_id]

# Function to calculate nutritional needs based on mealtime, diseases, and basic calorie intake
def hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input_list, jenis_kelamin):
    faktor = hitung_kebutuhan_faktor(meal_id)
    penyakit_input = set(penyakit_input_list)
    kebutuhan_kalori = protein = lemak = lemak_jenuh = lemak_tidak_jenuh_ganda = lemak_tidak_jenuh_tunggal = karbohidrat = kolesterol = gula = serat = garam = kalium = 0

    if {'Diabetes', 'Hipertensi', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        print("Nutrisi yang dibutuhkan untuk mealtime", meal_id, ":", nutrisi)
        print("Digabung semua")
        return nutrisi

    if {'Diabetes', 'Hipertensi'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        print("Diabetes dan Hipertensi")
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        return nutrisi
    
    if {'Diabetes', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.55 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 1500
        kalium = faktor * 3500
        print("Diabetes dan Kolesterol")
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        return nutrisi
    
    if {'Hipertensi', 'Kolesterol'}.issubset(penyakit_input):
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.2 * kebutuhan_kalori / 9
        lemak_jenuh = 0.05 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.6 * kebutuhan_kalori / 4
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 2400
        kalium = faktor * 3500
        print("Hipertensi dan Kolesterol")
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        return nutrisi
    
    if 'None' in penyakit_input:  # Asumsi 'Zone' ditambahkan dalam input jika pengguna mengikuti diet Zone
        kebutuhan_kalori = faktor * AKEi
        protein = 0.3 * kebutuhan_kalori / 4  # 30% kalori dari protein, setiap gram protein = 4 kalori
        lemak = 0.3 * kebutuhan_kalori / 9  # 30% kalori dari lemak, setiap gram lemak = 9 kalori
        lemak_jenuh = 0.05 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.4 * kebutuhan_kalori / 4  # 40% kalori dari karbohidrat, setiap gram karbo = 4 kalori
        kolesterol = faktor * 200  # Kolesterol bisa disesuaikan berdasarkan faktor risiko lain
        gula = 0.025 * kebutuhan_kalori  # Gula tetap dijaga rendah
        serat = faktor * 30  # Serat tinggi untuk mendukung kesehatan pencernaan dan kardiovaskular
        garam = faktor * 1500  # Pembatasan garam untuk mendukung kesehatan jantung
        kalium = faktor * 3500  # Kalium tinggi untuk keseimbangan elektrolit
        print("None")
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        return nutrisi
      
    if 'Diabetes' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.225 * kebutuhan_kalori / 4
        lemak = 0.25 * kebutuhan_kalori / 9
        lemak_jenuh = 0.09 * lemak 
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.65 * kebutuhan_kalori / 4
        kolesterol = faktor * 300
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 25
        garam = faktor * 3000
        kalium = faktor * 3500
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        print("Nutrisi yang dibutuhkan untuk mealtime", meal_id, ":", nutrisi)
        print("Nutrisi yang dibutuhkan untuk mealtime", meal_id, ":")
        print("Kalori:", kebutuhan_kalori, "kkal")
        print("Protein:", protein, "g")
        print("Lemak Total:", lemak, "g")
        print("Lemak Jenuh:", lemak_jenuh, "g")
        print("Lemak Tidak Jenuh Ganda:", lemak_tidak_jenuh_ganda, "g")
        print("Lemak Tidak Jenuh Tunggal:", lemak_tidak_jenuh_tunggal, "g")
        print("Karbohidrat:", karbohidrat, "g")
        print("Kolesterol:", kolesterol, "mg")
        print("Gula:", gula, "g")
        print("Serat:", serat, "g")
        print("Garam:", garam, "mg")
        print("Kalium:", kalium, "mg")
        return nutrisi
    elif 'Hipertensi' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        lemak = 0.25 * kebutuhan_kalori / 9
        lemak_jenuh = 0.06 * lemak
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        karbohidrat = 0.625 * kebutuhan_kalori / 4
        kolesterol = faktor * 300
        gula = 0.025 * kebutuhan_kalori
        serat = faktor * 12.5
        garam = faktor * 2400
        kalium = faktor * 3500
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        print("Nutrisi yang dibutuhkan untuk mealtime", meal_id, ":", nutrisi)
        return nutrisi
    elif 'Kolesterol' in penyakit_input:
        kebutuhan_kalori = faktor * AKEi
        protein = 0.125 * kebutuhan_kalori / 4
        karbohidrat = 0.65 * kebutuhan_kalori / 4
        lemak = 0.225 * kebutuhan_kalori / 9
        lemak_jenuh = 0.06 * kebutuhan_kalori / 9
        lemak_tidak_jenuh_ganda = 0.1 * lemak
        lemak_tidak_jenuh_tunggal = lemak - lemak_jenuh - lemak_tidak_jenuh_ganda
        kolesterol = faktor * 200
        gula = 0.025 * kebutuhan_kalori
        if jenis_kelamin.lower() == 'laki-laki':
            serat = faktor * 38
        elif jenis_kelamin.lower() == 'perempuan':
            serat = faktor * 25
        else:
           raise ValueError("Jenis kelamin tidak valid") 
        garam = faktor * 2400
        kalium = faktor * 3500
        nutrisi = np.array([[kebutuhan_kalori, protein, lemak, lemak_jenuh, lemak_tidak_jenuh_ganda, lemak_tidak_jenuh_tunggal, karbohidrat, kolesterol, gula, serat, garam, kalium]])
        print("Nutrisi yang dibutuhkan untuk mealtime", meal_id, ":", nutrisi)
        return nutrisi
    else:
        return ValueError("Penyakit tidak valid")

def rekomendasi_makanan(dataset, penyakit_input, alergi_input, AKEi, jenis_kelamin):
    rekomendasi_akhir = pd.DataFrame()

    # Filter resep yang sesuai dengan penyakit dan alergi (nilai 0)
    for penyakit in penyakit_input:
        dataset = dataset[dataset[penyakit] == 0]
        
    # Filter resep yang sesuai dengan alergi (nilai 0)
    for alergi in alergi_input:
        dataset = dataset[dataset[alergi] == 0]

    for meal_id in [1, 2, 3]:  # Loop through meal times: 1 - breakfast, 2 - lunch, 3 - dinner
        # Hitung kebutuhan nutrisi untuk setiap mealtime
        nutrisi_dibutuhkan = hitung_kebutuhan_nutrisi(meal_id, AKEi, penyakit_input, jenis_kelamin)
        
        # Filter resep yang sesuai dengan mealtime yang sesuai
        dataset_mealtime = dataset[dataset['Meal ID'] == meal_id]

        # Mengambil fitur nutrisi dari subset dataset
        nutrisi_columns = ['Energi (kkal)', 'Protein (g)', 'Lemak (g)', 'Lemak Jenuh (g)', 'Lemak tak Jenuh Ganda (g)', 'Lemak tak Jenuh Tunggal (g)', 'Karbohidrat (g)', 'Kolesterol (mg)', 'Gula (g)', 'Serat (g)', 'Sodium (mg)', 'Kalium (mg)']
        
        if not all(col in dataset_mealtime.columns for col in nutrisi_columns):
            raise ValueError(f"Dataset tidak memiliki kolom nutrisi yang diperlukan: {nutrisi_columns}")

        X_mealtime = dataset_mealtime[nutrisi_columns]
        
        # Menskalakan fitur
        scaler = MinMaxScaler()
        X_mealtime_scaled = scaler.fit_transform(X_mealtime)
        
        # Membuat DataFrame untuk input nutrisi yang dibutuhkan dengan nama kolom yang sesuai
        nutrisi_dibutuhkan_df = pd.DataFrame(nutrisi_dibutuhkan, columns=nutrisi_columns)
        
        # Menskalakan nutrisi yang dibutuhkan
        nutrisi_dibutuhkan_scaled = scaler.transform(nutrisi_dibutuhkan_df)

        # Filter resep berdasarkan nutrisi yang dibutuhkan (nilai dibawah nutrisi yang dibutuhkan)
        mask = np.all(X_mealtime_scaled <= nutrisi_dibutuhkan_scaled, axis=1)
        rekomendasi = dataset_mealtime[mask]
        
        # Debugging untuk melihat hasil filter nutrisi
        print(f"Rekomendasi setelah filter nutrisi untuk mealtime {meal_id}: {len(rekomendasi)} resep")
        print(rekomendasi[['Nama Resep', 'Meal ID', 'Protein (g)', 'Lemak (g)', 'Karbohidrat (g)']])
        
        rekomendasi_akhir = pd.concat([rekomendasi_akhir, rekomendasi])
    
    return rekomendasi_akhir

# Contoh penggunaan
# Tentukan input pengguna
penyakit_input = 'None'.split(",")
alergi_input = 'Seafood'.split(",")
jenis_kelamin = "laki-laki"
AKEi = hitung_AKEi_umur(Bb=70, Tb=170, jenis_kelamin=jenis_kelamin, umur=30)

# Panggil fungsi rekomendasi_makanan
rekomendasi_resep = rekomendasi_makanan(dataset, penyakit_input, alergi_input, AKEi, jenis_kelamin)

# Debugging untuk melihat hasil akhir rekomendasi
print(f"Total rekomendasi: {len(rekomendasi_resep)} resep")
print(rekomendasi_resep[['Nama Resep', 'Meal ID', 'Protein (g)', 'Lemak (g)', 'Karbohidrat (g)']])
