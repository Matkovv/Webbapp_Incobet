import json
from geopy.distance import geodesic

# Współrzędne Warszawy
warsaw_location = (52.2297, 21.0122)

# Flota gruszek
gruszki_capacity = {
    "gruszka_3_5": 3.5,
    "gruszka_6_5": 6.5,
    "gruszka_9": 9.0
}

gruszki_available = {
    "gruszka_3_5": 3,
    "gruszka_6_5": 2,
    "gruszka_9": 2
}

def load_locations(filename):
    try:
        with open(filename, 'r') as json_file:
            locations = json.load(json_file)
        return {city: tuple(coords) for city, coords in locations.items()}
    except FileNotFoundError:
        print("Nie znaleziono pliku locations.json")
        return {}

def calculate_trucks_and_courses(cubic_meters):
    total_capacity = sum(gruszki_available[type_] * gruszki_capacity[type_] for type_ in gruszki_available)
    required_trucks = cubic_meters / total_capacity
    full_courses_needed = int(required_trucks) + (1 if cubic_meters % total_capacity > 0 else 0)

    # Przydzielanie gruszek
    truck_assignment = {}
    remaining_cubic_meters = cubic_meters

    for type_, capacity in sorted(gruszki_capacity.items(), key=lambda x: -x[1]):
        available_count = gruszki_available[type_]
        while available_count > 0 and remaining_cubic_meters > 0:
            if remaining_cubic_meters >= capacity:
                truck_assignment[type_] = truck_assignment.get(type_, 0) + 1
                remaining_cubic_meters -= capacity
                available_count -= 1
            else:
                break

    return truck_assignment, remaining_cubic_meters, full_courses_needed

def calculate_distance(location):
    return geodesic(location, warsaw_location).kilometers

# Użytkownik wprowadza dane
def main():
    bet_type = input("Podaj rodzaj betonu: ")
    cubic_meters = float(input("Podaj ilość betonu w metrach sześciennych: "))
    city = input("Podaj lokalizację (miasto w Polsce): ")

    if city in locations:
        location_coords = locations[city]
        distance = calculate_distance(location_coords)

        truck_assignment, remaining, total_courses = calculate_trucks_and_courses(cubic_meters)

        print(f"\nRodzaj betonu: {bet_type}")
        print(f"Ilość betonu: {cubic_meters} m³")
        print(f"Lokalizacja: {city}")
        print(f"Odległość od Warszawy: {distance:.2f} km")

        if remaining > 0:
            print(f"\nPrzewożenie całego betonu wymaga {total_courses} kursów.")
            print("Niestety nie wszystkie gruszki są dostępne na raz.")
            print("Potrzebne gruszki:")
            for truck_type, count in truck_assignment.items():
                print(
                    f"- {count} x Gruszka {truck_type.replace('_', ' ')} (pojemność: {gruszki_capacity[truck_type]} m³)")
            print(f"Wymagana objętość betonu do transportu w kolejnych kursach: {remaining:.2f} m³")
        else:
            print("\nWszystek beton można transportować w jednym kursie.")
            print("Potrzebne gruszki:")
            for truck_type, count in truck_assignment.items():
                print(
                    f"- {count} x Gruszka {truck_type.replace('_', ' ')} (pojemność: {gruszki_capacity[truck_type]} m³)")
    else:
        print("Nieznana lokalizacja. Proszę podać miasto z listy.")


if __name__ == "__main__":
    main()
