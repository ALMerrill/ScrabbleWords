from flask import Flask, request, jsonify
import os
import socket
from word_generation import generator
from nearest_neighbor import nearest_neighbor, markov
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

model, vectors = nearest_neighbor.load_model('fil9.vec')
dictionary_markov_model = markov.get_dictionary_model()


@app.route('/')
def root():
    return '<h3>Flask is up and running<h3>'


@app.route('/api/definition')
@cross_origin()
def definition():
    letters = request.args.get('letters', default='', type=str)
    if letters == '':
        return 'No letters were given'

    best_word = generator.generate(letters)
    results = nearest_neighbor.nearest_neighbors(model, best_word, vectors)
    definitions = nearest_neighbor.get_definitions(results)
    combined_markov_model = markov.get_combined_model(
        dictionary_markov_model, definitions)
    return jsonify({
        'word': best_word,
        'definition': combined_markov_model.make_sentence()
    })


if __name__ == '__main__':
    app.run(host='localhost', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
