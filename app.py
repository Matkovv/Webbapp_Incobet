from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from dashboard.routes import dashboard
from kalkulator import load_locations, calculate_trucks_and_courses, calculate_distance  # Import funkcji z kalkulator.py

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.register_blueprint(dashboard, url_prefix='/dashboard')

# Wczytaj lokalizacje z pliku
locations = load_locations('locations.json')

class Beton(db.Model):
    __tablename__ = 'beton'
    id = db.Column(db.Integer, primary_key=True)
    rodzaj = db.Column(db.String(100), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Beton {self.rodzaj}>'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

def init_db():
    # Sprawdź, czy użytkownik 'admin' już istnieje
    existing_user = User.query.filter_by(username='admin').first()
    if not existing_user:
        hashed_password = generate_password_hash('admin', method='pbkdf2:sha256')
        admin_user = User(username='admin', password=hashed_password)
        db.session.add(admin_user)
        db.session.commit()
    else:
        print("Użytkownik 'admin' już istnieje, pominięto dodanie.")

def create_tables():
    db.create_all()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        rodzaj = request.form['rodzaj']
        ilosc = request.form['ilosc']
        if rodzaj and ilosc:
            nowy_beton = Beton(rodzaj=rodzaj, ilosc=int(ilosc))
            db.session.add(nowy_beton)
            db.session.commit()
            return redirect(url_for('dashboard'))

    betony = Beton.query.all()
    return render_template('dashboard.html', betony=betony)

@app.route('/beton_app', methods=['GET', 'POST'])
def beton_app():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password'

    return render_template('beton_app.html')

@app.route('/manage_betony', methods=['GET', 'POST'])
def manage_betony():
    if not session.get('logged_in'):
        return redirect(url_for('beton_app'))

    if request.method == 'POST':
        rodzaj_betonu = request.form.get('rodzaj_betonu')
        ilosc = float(request.form.get('ilosc'))
        if Beton.query.filter_by(rodzaj=rodzaj_betonu).first():
            return 'Beton o tej nazwie już istnieje', 400
        new_beton = Beton(rodzaj=rodzaj_betonu, ilosc=ilosc)
        db.session.add(new_beton)
        db.session.commit()
        return redirect(url_for('manage_betony'))

    betony = Beton.query.all()
    return render_template('manage_betony.html', betony=betony)

@app.route('/kalkulator', methods=['GET', 'POST'])
def kalkulator_route():
    if request.method == 'POST':
        bet_type = request.form.get('rodzaj_betonu')
        cubic_meters = float(request.form.get('ilosc_betonu', 0))
        city = request.form.get('lokalizacja')

        bet = Beton.query.filter_by(rodzaj=bet_type).first()
        if not bet or cubic_meters > bet.ilosc:
            return jsonify({'error': 'Niewystarczająca ilość betonu w magazynie.'}), 400

        if city in locations:
            location_coords = locations[city]
            distance = calculate_distance(location_coords)
            truck_assignment, remaining, total_courses = calculate_trucks_and_courses(cubic_meters)

            return jsonify({
                'bet_type': bet_type,
                'cubic_meters': cubic_meters,
                'city': city,
                'distance': distance,
                'truck_assignment': truck_assignment,
                'remaining': remaining,
                'total_courses': total_courses
            })

        return jsonify({'error': 'Nieznana lokalizacja. Proszę podać miasto z listy.'}), 400

    return render_template('kalkulator.html', locations=locations)

@app.route('/o_firmie', methods=['GET', 'POST'])
def o_firmie():
    return render_template('o_firmie.html')

@app.route('/realizacje', methods=['GET', 'POST'])
def realizacje():
    return render_template('realizacje.html')

@app.route('/technologia', methods=['GET', 'POST'])
def technologia():
    return render_template('technologia.html')

@app.route('/oferta', methods=['GET', 'POST'])
def oferta():
    return render_template('oferta.html')

@app.route('/kontakt', methods=['GET', 'POST'])
def kontakt():
    return render_template('kontakt.html')

if __name__ == '__main__':
    with app.app_context():
        create_tables()
        init_db()
    app.run(debug=True)
