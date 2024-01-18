"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
from models import People, Planets

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/people', methods=['GET'])
def get_people():
    response_body = {
        'id': People.id,
        'name': People.name,
        'height': People.height,
        'mass': People.mass,
        'hair_color': People.hair_color,
        'skin_color': People.skin_color,
        'eye_color': People.eye_color,
        'birth_year': People.birth_year,
        'gender': People.gender,
        'homeworld': People.homeworld
    }
    return jsonify(response_body), 200

@app.route('/planets', methods=['GET'])
def get_people():
    response_body = {
        'id': Planets.id,
        'name': Planets.name,
        'rotation_period': Planets.rotation_period,
        'orbital_period': Planets.orbital_period,
        'diameter': Planets.diameter,
        'climate': Planets.climate,
        'gravity': Planets.gravity,
        'terrain': Planets.terrain,
        'surface_water': Planets.surface_water,
        'population': Planets.population
    }
    return jsonify(response_body), 200

@app.route('/user/favorites', methods=['GET'])
def get_favorites():
    planet_favorite = User.planet_favorite
    people_favorite = User.people_favorite
    favorites = Planets.query.filter(
        (Planets.id.ilike(planet_favorite))
    ) & People.query.filter(
        (People.id.ilike(people_favorite))
    )
    return jsonify(favorites), 200

@app.route('/user/favorites/<int:people_id>')
def get_one_person(id):
        person = People.query.get_or_404(id)
        return jsonify(person), 200

@app.route('/user/favorites/<int:planets_id>')
def get_one_planet(id):
        planet = Planets.query.get_or_404(id)
        return jsonify(planet), 200

@app.route('/user', methods=['GET'])
def get_users():
    response_body = {
        "id": User.id,
        "email": User.email,
        "password": User.password,
        "is_active": User.is_active
    }
    return jsonify(response_body), 200

@app.route('/favorite/planets/<int:planets_id>', methods=['POST', 'DELETE'])
def add_or_remove_planet_to_favorites(user_id, planet_id):
     user = User.query.get_or_404(user_id)
     if request.method == 'DELETE': 
          planeta_eliminado = user.planet_favorite(planet_id)
          db.session.delete(planeta_eliminado)
          db.session.comit()
          return jsonify({"message": "Planeta eliminado de favoritos"})
     else:
        nuevo_Favorito = user(planet_id=planet_id)
        db.session.add(nuevo_Favorito)
        db.session.commit()
        return jsonify({"message": "Planeta añadido a favoritos"})
     
     

@app.route('/favorite/people/<int:people_id>', methods=['POST', 'DELETE'])
def add_or_remove_planet_to_favorites(user_id, people_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'DELETE': 
          persona_eliminada = user.people_favorite(people_id)
          db.session.delete(persona_eliminada)
          db.session.comit()
          return jsonify({"message": "Persona eliminada de favoritos"})
    else:
        nuevo_Favorito = user(people_id=people_id)
        db.session.add(nuevo_Favorito)
        db.session.commit()
        return jsonify({"message": "Persona añadida a favoritos"})

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
