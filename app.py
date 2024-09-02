from flask import Flask, render_template, request, jsonify
import kalkulator  # Upewnij się, że kalkulator.py jest w tym samym folderze

app = Flask(__name__)
locations = kalkulator.load_locations('locations.json')  # Wczytaj lokalizacje z pliku JSON


# Przykładowe dane betonu, symulujące bazę danych
beton_info = {
    "C6/8": "Beton C6/8 to beton o niskiej wytrzymałości, idealny do małych projektów.",
    "C8/10": "Beton C8/10 to beton o średniej wytrzymałości, używany w budownictwie ogólnym.",
    "C10/12": "Beton C10/12 to uniwersalny beton, doskonały zarówno do budowy fundamentów, jak i konstrukcji.",
    "C12/16": "Beton C12/16 to beton o wysokiej wytrzymałości, idealny do konstrukcji nośnych."
}

@app.route('/')
def home():
    return render_template('index.html')  # Strona główna

@app.route('/beton_app', methods=['GET', 'POST'])
def beton_app():
    return render_template('beton_app.html')

# @app.route('/kalkulator', methods=['GET', 'POST'])
# def kalkulator():
    # return render_template('kalkulator.html')

@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator_route():
    if request.method == 'POST':
        bet_type = request.form.get('rodzaj_betonu')
        cubic_meters = float(request.form.get('ilosc_betonu', 0))
        city = request.form.get('lokalizacja')

        if city in locations:
            location_coords = locations[city]
            distance = kalkulator.calculate_distance(location_coords)
            truck_assignment, remaining, total_courses = kalkulator.calculate_trucks_and_courses(cubic_meters)

            # Respond with JSON for AJAX requests
            return jsonify({
                'bet_type': bet_type,
                'cubic_meters': cubic_meters,
                'city': city,
                'distance': distance,
                'truck_assignment': truck_assignment,
                'remaining': remaining,
                'total_courses': total_courses
            })

        # Handle unknown location
        return jsonify({'error': 'Nieznana lokalizacja. Proszę podać miasto z listy.'}), 400

    # Always handle GET requests
    return render_template('kalkulator.html', locations=locations)  # Przekazanie lokalizacji do szablonu




@app.route('/o_firmie', methods=['GET', 'POST'])
def o_firmie():
    return render_template('o_firmie.html') # strona o_firmie

@app.route('/realizacje', methods=['GET', 'POST'])
def realizacje():
    return render_template('realizacje.html')

@app.route('/technologia', methods=['GET', 'POST'])
def technologia():
    return render_template('technologia.html')

@app.route('/oferta', methods=['GET', 'POST'])
def oferta():
    return render_template('oferta.html')  # Strona oferty

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    return render_template('kontakt.html')

# @app.route('/test', methods=['GET', 'POST'])
# def test():
#     transport_info = None
#     beton_description = None
#
#     # Obsługa formularza post
#     if request.method == 'POST':
#         rodzaj_betonu = request.form.get('rodzaj_betonu')
#         if rodzaj_betonu in beton_info:
#             beton_description = beton_info[rodzaj_betonu]  # Pobierz opis betonu
#         ilosc_betonu = float(request.form.get('ilosc_betonu')) if request.form.get('ilosc_betonu') else 0
#
#         # Logika obliczeń transportu
#         transport_needed = ''
#         if ilosc_betonu <= 3.5 * 4:  # 4 gruszki 3,5m³
#             trucks_needed = (ilosc_betonu / 3.5)
#             transport_needed = f'Potrzebne gruszki: {trucks_needed:.0f} x 3,5m³ Gruszki'
#         elif ilosc_betonu <= 9 * 2:  # 2 gruszki 9m³
#             trucks_needed = (ilosc_betonu / 9)
#             transport_needed = f'Potrzebne gruszki: {trucks_needed:.0f} x 9m³ Gruszki'
#         else:  # Pompogruszka 12m³
#             trucks_needed = (ilosc_betonu / 12)
#             transport_needed = f'Potrzebna pompogruszka: 1 x 12m³, wymagane dodatkowe ładunki gruszki: {ilosc_betonu - 12:.2f} m³'
#
#         transport_info = {
#             "rodzaj_betonu": rodzaj_betonu,
#             "transport_needed": transport_needed,
#             "czas_dostawy": "24 godziny"  # Przykładowy czas dostawy
#         }
#
#     return render_template('test.html', transport_info=transport_info, beton_description=beton_description)

if __name__ == '__main__':
    app.run(debug=True)
