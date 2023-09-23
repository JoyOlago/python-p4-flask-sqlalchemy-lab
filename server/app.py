#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Zookeeper, Enclosure, Animal

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Zoo app</h1>'

@app.route('/animal/<int:id>')
def animal_by_id(id):
    animal = Animal.query.get_or_404(id)
    
    response_body = f''''
        <h1>Information for {animal.name}</h1>
        <h2>Species: {animal.species}</h2>
        <h2>Zookeeper: {animal.zookeeper.name if animal.zookeeper else "N/A"}</h2>
        <h2>Enclosure: {animal.enclosure.environment if animal.enclosure else "N/A"}</h2>
    '''
    
    response = make_response(response_body, 200)
    return response

@app.route('/zookeeper/<int:id>')
def zookeeper_by_id(id):
    zookeeper = Zookeeper.query.get_or_404(id)
    
    response_body = f'<h1>Information for {zookeeper.name}</h1>'
    response_body += f'<h2>Birthday: {zookeeper.birthday.strftime("%Y-%m-%d") if zookeeper.birthday else "N/A"}</h2>'
    
    animals = [animal.name for animal in zookeeper.animals.all()]
    if not animals:
        response_body += f'<h2>Takes care of no animals at this time.</h2>'
    else:
        response_body += f'<h2>Takes care of the following animals:</h2>'
        for animal in animals:
            response_body += f'<p>{animal}</p>'

    response = make_response(response_body, 200)
    return response

@app.route('/enclosure/<int:id>')
def enclosure_by_id(id):
    nclosure = Enclosure.query.get_or_404(id)
    
    response_body = f'<h1>Information for enclosure</h1>'
    response_body += f'<h2>Environment: {enclosure.environment}</h2>'
    response_body += f'<h2>Open to Visitors: {"Yes" if enclosure.open_to_visitors else "No"}</h2>'
    
    animals = [animal.name for animal in enclosure.animals.all()]
    if not animals:
        response_body += f'<h2>No animals in this enclosure at this time.</h2>'
    else:
        response_body += f'<h2>Animals in this enclosure:</h2>'
        for animal in animals:
            response_body += f'<p>{animal}</p>'

    response = make_response(response_body, 200)
    return response



if __name__ == '__main__':
    app.run(port=5555, debug=True)
