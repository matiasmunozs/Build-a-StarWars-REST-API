import json
from flask import Flask, render_template, request, jsonify
from flask_migrate import Migrate
from flask_cors import CORS
from models import db, User, Character, Planet


#pipenv install flask flask-migrate flask-sqlalchemy flask-cors flask-jwt-extended 
#Para este code no usare el jwt

app = Flask(__name__)
app.url_map.slashes = False
app.config['DEBUG'] = True
app.config['ENV'] = 'development'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'


db.init_app(app)
Migrate(app, db)
CORS(app)



@app.route('/')
def root():
    return render_template('index.html')


@app.route('/user', methods=['POST'])
def add_user():

    email=request.json.get('email')
    username=request.json.get('username')
    password=request.json.get('password', '')

    
    users = User()
    users.email = email
    users.username = username
    users.password = password
    users.save()

    return jsonify({ "msg": "User Added Successfully" }), 201



@app.route('/users', methods=['GET']) 
def get_users():
    users = User.query.all()
    users = list(map(lambda user: user.serialize(), users))

    return jsonify(users), 200

@app.route('/people', methods=['GET'])
def get_characters():
    characters = Character.query.all()
    characters = list(map(lambda character: character.serialize(), characters))

    return jsonify(characters), 200


@app.route('/people/<int:id>', methods=['GET'])
def get_character(id):
 
    characters = Character.query.get(id)

    if characters is None:
        return jsonify({"msg":"This character does not exist. Lo siento."})

    return jsonify(characters.serialize()), 200


@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    planets = list(map(lambda planet: planet.serialize(), planets))

    return jsonify(planets), 200

@app.route('/planets/<int:id>', methods=['GET'])
def get_planet(id):
 
    planet = Planet.query.get(id)

    if planet is None:
        return jsonify({"msg":"This Planet doesn't exist. Lo siento"})

    return jsonify(planet.serialize()), 200

@app.route('/users/favorites', methods=['GET'])
def get_fav_characters():

    characters = User.query.get('people')
    

    if characters is None:
        return jsonify({"msg":"You do not have any Favorite, please add with your POST"})

    return jsonify(characters.serialize_with_favorites()), 200


@app.route('/users/favorites/people', methods=['POST'])
def add_fav_character():

    
    name=request.json.get('name')
    description=request.json.get('description', '')

    
    character = Character()
    character.name = name
    character.description = description
    character.save()

    return jsonify({ "msg": "Favorite Character Added Successfully" }), 201


@app.route('/users/favorites/planet', methods=['POST'])
def add_favorite_planet():

    
    name=request.json.get('name')
    description=request.json.get('description', '')

    
    planet = Planet()
    planet.name = name
    planet.description = description
    planet.save()

    return jsonify({ "msg": "Favorite Planet Added Successfully" }), 201


@app.route('/users/favorites/people/<int:id>', methods=['DELETE'])
def delete_favorite_character(id):
    character_id = Character.query.get(id)

    character_id.delete()

    return jsonify({ "msg" : "Favorite Character deleted "})


@app.route('/users/favorites/planets/<int:id>', methods=['DELETE'])
def delete_favorite_planet(id):
    planet = Planet.query.get(id)

    planet.delete()

    return jsonify({ "msg" : "Favorite Planet deleted "})



if __name__ == '__main__':
    app.run()
