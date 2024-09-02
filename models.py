from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Beton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rodzaj = db.Column(db.String(100), nullable=False)
    ilosc = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Beton {self.rodzaj}>'
