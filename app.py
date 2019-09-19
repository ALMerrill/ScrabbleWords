from flask import Flask, request, jsonify
import os
import socket
from nearest_neighbor import nearest_neighbor
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

model, vectors = nearest_neighbor.load_model('fil9.vec')


@app.route('/')
def root():
    return '<h3>Flask is up and running<h3>'


@app.route('/api/definition')
@cross_origin()
def definition():
    word = request.args.get('word', default='', type=str)
    if word == '':
        return 'No word was given'

    results = nearest_neighbor.nearest_neighbors(model, word, vectors)
    definitions = nearest_neighbor.get_definitions(results)
    with open('word_generation/definitions.txt', 'w+') as f:
        for key in definitions:
            for definition in definitions[key]:
                f.write(definition + '\n')

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='localhost', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
