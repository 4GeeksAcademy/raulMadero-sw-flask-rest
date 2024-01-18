from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.string(45), nullable=False, unique=False)
    height = db.Column(db.String(45), nullable=False, unique=False)
    mass = db.Column(db.String(45), nullable=False, unique=False)
    hair_color: db.Column(db.String(45), nullable=False, unique=False)
    skin_color: db.Column(db.String(45), nullable=False, unique=False)
    eye_color: db.Column(db.String(45), nullable=False, unique=False)
    birth_year: db.Column(db.String(45), nullable=False, unique=False)
    gender: db.Column(db.String(45), nullable=False, unique=False)
    homeworld: db.Column(db.String(45), nullable=False, unique=False)

class Planets(db.Model):
    id: db.Column(db.Integer, primary_key=True)
    name: db.Column(db.String(45), nullable=False, unique=False)
    rotation_period: db.Column(db.String(45), nullable=False, unique=False)
    orbital_period: db.Column(db.String(45), nullable=False, unique=False)
    diameter: db.Column(db.String(45), nullable=False, unique=False)
    climate: db.Column(db.String(45), nullable=False, unique=False)
    gravity: db.Column(db.String(45), nullable=False, unique=False)
    terrain: db.Column(db.String(45), nullable=False, unique=False)
    surface_water: db.Column(db.String(45), nullable=False, unique=False)
    population: db.Column(db.String(45), nullable=False, unique=False)
    

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    planet_favorite = db.Column(db.Integer, db.ForeignKey('planets.id'))
    colaborador = db.relationship('Planets')
    people_favorite = db.Column(db.Integer, db.ForeignKey('people.id'))
    colaborador = db.relationship('People')

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }