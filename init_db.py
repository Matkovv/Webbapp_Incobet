import sqlite3

# Utworzenie bazy danych i tabeli
connection = sqlite3.connect('database.db')  # Tworzy lub otwiera plik database.db
cursor = connection.cursor()

# Twórz tabelę messages, jeśli nie istnieje
cursor.execute('''
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- Automatyczne zwiększanie identyfikatora
        message TEXT NOT NULL                    -- Treść wiadomości (nie może być NULL)
    )
''')

connection.commit()  # Zatwierdź zmiany do bazy danych
connection.close()   # Zamknij połączenie
