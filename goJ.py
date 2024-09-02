import json

# Słownik z miastami i ich współrzędnymi
locations = {
    "Warszawa": (52.2297, 21.0122),
    "Kraków": (50.0647, 19.9450),
    "Wrocław": (51.1079, 17.0385),
    "Łódź": (51.7592, 19.4560),
    "Gdańsk": (54.3520, 18.6466),
    "Poznań": (52.4084, 16.9340),
    "Katowice": (50.2586, 19.0213),
    "Lublin": (51.2465, 22.5685),
    "Białystok": (53.1325, 23.1688),
    "Szczecin": (53.4285, 14.5530),
    "Bydgoszcz": (53.1235, 18.0084),
    "Toruń": (53.0152, 18.5984),
    "Zielona Góra": (51.9353, 15.5063),
    "Częstochowa": (50.8114, 19.1242),
    "Radom": (51.4025, 21.1478),
    "Rzeszów": (50.0411, 21.9991),
    "Olsztyn": (53.7792, 20.4905),
    "Opole": (50.6645, 17.9285),
    "Elbląg": (54.1522, 19.3938),
    "Koszalin": (54.1756, 16.1855),
    "Kielce": (50.8661, 20.6289),
    "Słupsk": (54.4657, 17.0360),
    # Dodaj więcej miast tutaj...
}

# Konwertuj współrzędne na listy, aby były serializowane poprawnie
locations_list = {city: list(coords) for city, coords in locations.items()}

# Zapisz słownik do pliku locations.json
with open('locations.json', 'w') as json_file:
    json.dump(locations_list, json_file, indent=4)

print("Słownik miast został zapisany w pliku locations.json.")
