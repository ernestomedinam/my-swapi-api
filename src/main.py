"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
import requests
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import Character, db, User


app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
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

@app.route('/user', methods=['GET'])
def handle_hello():

    response_body = {
        "msg": "Hello, this is your GET /user response "
    }

    return jsonify(response_body), 200

@app.route('/characters/<int:id>')
def handle_one_character(id):
    character = Character.query.get(id)
    if character is None:
        return jsonify({
            "msg": "not found"
        }), 404
    return jsonify(character.serialize()), 200

@app.route('/characters', methods=["GET", "POST"])
def handle_characters():
    if request.method == "GET":
        characters = Character.query.all()
        return jsonify(list(map(
            lambda character: character.shortalize(),
            characters
        ))), 200
    else:
        body = request.json
        character = Character.create(
            name=body['name'],
            eye_color=body['eye_color']
        )
        dictionary = character.serialize()
        return jsonify(dictionary), 201

BASE_URL = "https://www.swapi.tech/api/"

@app.route('/populate-characters', methods=["POST"])
def populate_characters():

    # solicitud de todos los characters
    response = requests.get(
        f"{BASE_URL}{'people'}/?page=1&limit=100"
    )

    # cuerpo de esa solicitud con results que es
    # una lista de characters con data resumida
    body = response.json()
    all_characters = []
    
    # ciclo a traves de la lista body['results']
    # donde cada result es un diccionario resumido
    # de un character, segun swapi
    for result in body['results']:
        
        # solicitud del detalle del character result
        response = requests.get(result['url'])
        body = response.json()

        # agregamos a la lista las propiedades de este
        # character
        all_characters.append(body['result']['properties'])
    
    instances = []
    
    # recorremos la lista all_characters que son
    # diccionarios de propiedades de cada personaje
    for character in all_characters:
        
        # creamos la instancia y se guarda en bdd
        instance = Character.create(character)

        # agregamos el OBJETO character a la lista
        instances.append(instance)

    # mapeamos la lista instances para obtener una lista
    # de diccionarios que represente a cada objeto
    # character; convertimos el objeto map en una lista
    # y jsonificamos y devolvemos el resultado
    return jsonify(list(map(
        lambda inst: inst.serialize(),
        instances
    ))), 200



# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

with app.app_context():
    from populate_db import populate_db
