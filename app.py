from flask import Flask
import os
import socket
import fasttext
import fasttext.util

app = Flask(__name__)


@app.route('/')
def root():
    return '<h3>Flask is up and running<h3>'


@app.route('/NN')
def tenNN():
    # TODO: move this logic to an util file
    model = fasttext.load_model('models/fil9-sg.bin')
    vectors = []

    with open('models/fil9-sg.vec') as vec_file:
        next(vec_file)
        j = 0
        for line in vec_file:
            j += 1
            vector = [float(i) for i in line.split()[1:]]
            vectors.append(vector)

    word_vec = model['asparagus']
    ban_set = []
    index = fasttext.util.find_nearest_neighbor(
        word_vec, vectors, ban_set)
    return model.words[index]


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
