from flask import Flask, request, jsonify
import os
import socket
from util import util

app = Flask(__name__)

model, vectors = util.load_model('fil9.bin')


@app.route('/')
def root():
    return '<h3>Flask is up and running<h3>'


@app.route('/api/nearest-neighbor')
def nearest_neighbor():
    # TODO: move this logic to an util file
    word = request.args.get('word', default='', type=str)
    if word == '':
        return 'No word was given'
    N = request.args.get('N', default=1, type=int)

    results = util.nearest_neighbor(model, word, vectors, N)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
