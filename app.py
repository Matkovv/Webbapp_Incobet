from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Funkcja do połączenia się z bazą danych
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Strona główna
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        message = request.form['message']
        conn = get_db_connection()
        conn.execute('INSERT INTO messages (message) VALUES (?)', (message,))
        conn.commit()
        conn.close()
        return redirect(url_for('home'))

    conn = get_db_connection()
    messages = conn.execute('SELECT * FROM messages').fetchall()
    conn.close()
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    app.run(debug=True)
