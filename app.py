from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')  # Główna strona

@app.route('/oferta')
def oferta():
    return render_template('oferta.html')  # Strona oferty

if __name__ == '__main__':
    app.run(debug=True)
