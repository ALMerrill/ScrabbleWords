from flask import Flask, request, jsonify
import os
import socket
from nearestNeighbor import nearestNeighbor

app = Flask(__name__)

model, vectors = nearestNeighbor.load_model('fil9.vec')


@app.route('/')
def root():
    return '<h3>Flask is up and running<h3>'


@app.route('/api/nearest-neighbor')
def nearest_neighbor():
    word = request.args.get('word', default='', type=str)
    if word == '':
        return 'No word was given'
    N = request.args.get('N', default=1, type=int)

    results = nearestNeighbor.nearest_neighbor(model, word, vectors, N)
    definitions = nearestNeighbor.get_definitions(results)
    with open('word_generation/definitions.txt', 'w+') as f:
        for key in definitions:
            for definition in definitions[key]:
                f.write(definition + '\n')

    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
