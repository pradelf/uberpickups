import pandas as pd
import requests
import time

# Charger ton fichier CSV original
df = pd.read_csv('taxi-zone-lookup.csv')

# Fonction pour interroger l'API Nominatim
def interroger_nominatim(zone, borough):
    adresse = f"{zone}, {borough}, New York"
    url = 'https://nominatim.openstreetmap.org/search'
    params = {
        'q': adresse,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }
    headers = {'User-Agent': 'MonApplicationGeocodage/1.0 (francis.pradel@gmail.com)'}
    response = requests.get(url, params=params, headers=headers)
    
    if response.status_code == 200:
        results = response.json()
        if results:
            latitude = results[0]['lat']
            longitude = results[0]['lon']
            return latitude, longitude
    return None, None

# Ajouter des colonnes latitude et longitude
df['latitude'] = None
df['longitude'] = None

# Remplir latitude et longitude
for index, row in df.iterrows():
    latitude, longitude = interroger_nominatim(row['Zone'], row['Borough'])
    df.at[index, 'latitude'] = latitude
    df.at[index, 'longitude'] = longitude
    print(f"{row['Zone']} => Latitude: {latitude}, Longitude: {longitude}")
    time.sleep(1)  # Respecte les conditions d'utilisation de Nominatim

# Sauvegarder le résultat
df.to_csv('taxi-zones-geocoded.csv', index=False)

