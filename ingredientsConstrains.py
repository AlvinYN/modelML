import pandas as pd

# Load the dataset
file_path = 'Cleaned_CombinedRecipe.csv'
data = pd.read_csv(file_path)

# Define the lists of ingredients that should be avoided for each condition
makanan_tidak_boleh_diabetes = [
    "Gula pasir", "Gula jawa", "Sirup", "Selai", "Jeli", "Buah awet gula",
    "Susu kental manis", "Minuman botol ringan", "Es krim", "Kue manis", "Dodol", 
    "Cake", "Tart", "Fast food", "Gorengan", "Ikan asin", "Telur asin", "MSG"
]

makanan_tidak_boleh_kolesterol = [
    "Kuning telur", "Hati" , "Ginjal", "Otak sapi", "Otak babi", "Cumi-cumi",
    "Mentega", "Krim", "Daging sapi", "Daging Kambing",
    "Kerang putih", "Tiram", "Santan", "Margarin", "Kue tar", "Es krim", "Sosis"
]

makanan_tidak_boleh_hipertensi = [
    "Otak", "Ginjal", "Lidah", "Daging asap", "Ham", "Dendeng", "Abon", "Keju", "Ikan asin", "Sardin", 
    "Ikan kaleng", "Kornet", "Ebi", "Udang kering", "Telur asin", "Telur pindang", "Saus tomat", "Petis", 
    "Sayur Kaleng", "Sawi asin", "Garam dapur", "Asinan", "Acar", "Buah kaleng", "Margarin", "Mentega", 
    "Minuman ringan", "Baking powder", "Soda kue", "Vetsin", "Kecap", "Terasi", "Kaldu instan", 
    "Tauco","Lemak hewan", "Keju", "Mentega", "Margarin", "Minyak kelapa", "Kuning telur", "Susu"
]

allergy_categories = {
    "Nuts": ["Kacang tanah", "Peanuts", "Kacang almond", "Almonds", "Kacang mete", "Cashews", "Kacang pistachio", "Pistachios", "Kacang kenari", "Walnuts", "Kacang pecan", "Pecans", "Kacang pinus", "Pine nuts", "Kacang brazil", "Brazil nuts", "Kacang macadamia", "Macadamia nuts", "Kacang hazelnut", "Hazelnuts"],
    "Eggs": ["Telur ayam", "Chicken eggs", "Telur bebek", "Duck eggs", "Telur angsa", "Goose eggs", "Telur puyuh", "Quail eggs", "Telur orak-arik", "Scrambled eggs", "Telur rebus", "Boiled eggs", "Telor", "Fried eggs", "Telur ceplok", "Omelette", "Telur mata sapi", "Omelet", "Telur"],
    "Seafood": ["Salmon", "Tuna", "Cod", "Trout", "Mackerel", "Sarden", "Sardine", "Anchovy", "Haddock", "Herring", "Halibut", "Udang", "Shrimp", "Lobster", "Kepiting", "Crab", "Kerang", "Clams", "Tiram", "Oysters", "Cumi-cumi", "Squid", "Gurita", "Octopus", "Kerang Simping", "Scallops", "Kerang Hijau", "Mussels", "Kerang Abalon", "Abalone"]
}

# Function to check if ingredients contain restricted items
def check_ingredients(ingredient_text, restriction_list):
    for item in restriction_list:
        if item.lower() in ingredient_text.lower():
            return 1
    return 0

# Apply the check function to create new columns
data['Diabetes'] = data['Ingredients'].apply(lambda x: check_ingredients(x, makanan_tidak_boleh_diabetes))
data['Kolesterol'] = data['Ingredients'].apply(lambda x: check_ingredients(x, makanan_tidak_boleh_kolesterol))
data['Hipertensi'] = data['Ingredients'].apply(lambda x: check_ingredients(x, makanan_tidak_boleh_hipertensi))
data['Nuts'] = data['Ingredients'].apply(lambda x: check_ingredients(x, allergy_categories['Nuts']))
data['Eggs'] = data['Ingredients'].apply(lambda x: check_ingredients(x, allergy_categories['Eggs']))
data['Seafood'] = data['Ingredients'].apply(lambda x: check_ingredients(x, allergy_categories['Seafood']))

# Combine disease columns into a single column
data['Diabetes,Kolesterol,Hipertensi'] = data.apply(lambda x: int(x['Diabetes'] == 0 and x['Kolesterol'] == 0 and x['Hipertensi'] == 0), axis=1)
data['Diabetes,Kolesterol'] = data.apply(lambda x: int(x['Diabetes'] == 0 and x['Kolesterol'] == 0), axis=1)
data['Diabetes,Hipertensi'] = data.apply(lambda x: int(x['Diabetes'] == 0 and x['Hipertensi'] == 0), axis=1)
data['Kolesterol,Hipertensi'] = data.apply(lambda x: int(x['Kolesterol'] == 0 and x['Hipertensi'] == 0), axis=1)

# Combine allergen columns into a single column
data['Nuts,Eggs'] = data.apply(lambda x: int(x['Nuts'] == 0 and x['Eggs'] == 0), axis=1)
data['Nuts,Seafood'] = data.apply(lambda x: int(x['Nuts'] == 0 and x['Seafood'] == 0), axis=1)
data['Eggs,Seafood'] = data.apply(lambda x: int(x['Eggs'] == 0 and x['Seafood'] == 0), axis=1)
data['Nuts,Eggs,Seafood'] = data.apply(lambda x: int(x['Nuts'] == 0 and x['Eggs'] == 0 and x['Seafood'] == 0), axis=1)

# Add a 'None' column with default values set to 0
data['None'] = 0

# Save the updated dataset to a new CSV file
updated_file_path = 'labeled_new_constrains.csv'
data.to_csv(updated_file_path, index=False)

print("Dataset has been labeled and saved successfully.")
