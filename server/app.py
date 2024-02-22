# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Pet

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False # Congifure the JSON module to not compact arrays/objects & to display each key/value pair on a separate line

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Welcome to the pet directory!'}
    return make_response(body, 200)
    # return make_response(
    #     '<h1>Welcome to the pet directory!</h1>',
    #     200
    # )


@app.route('/demo_json')
# This FN returns a JSON response w/ details of the 1st pet in the pets DB
def demo_json():
    # pet_json = '{"id": 1, "name" : "Fido", "species" : "Dog"}'
    pet = Pet.query.first() 
    # Below, we create a dictionary containing the pet's details
    pet_dict = {'id': pet.id, 
                'name': pet.name,
                'species': pet.species
                }
    # We pass the dict to make_response() to create & return a JSON response containing the dictionary
    return make_response(pet_dict, 200)


# This view gets pet data for a given ID value. 
@app.route('/pets/<int:id>') # The route takes ID as a parameter. 
def pet_by_id(id):
    pet = Pet.query.filter(Pet.id == id).first()
    if pet:
        body = {'id': pet.id,
                'name': pet.name,
                'species': pet.species
                }
        status = 200
    # Also includes an error response if pet is not found. 
    else: 
        body = {'message': f'Pet {id} not found.'}
        status = 404
    #Returns a JSON response containing the pet's details or an error message.
    return make_response(body, status) 


@app.route('/species/<string:species>')
def pet_by_species(species):
    pets = []
    for pet in Pet.query.filter_by(species=species).all():
        pet_dict = {'id': pet.id,
                    'name': pet.name,
                    }
        pets.append(pet_dict)
    body = {'count': len(pets),
            'pets': pets
            }
    return make_response(body, 200)
    



if __name__ == '__main__':
    app.run(port=5555, debug=True)
