from flask import Flask, request, jsonify
import os
import socket
import fasttext
import fasttext.util
import gensim

app = Flask(__name__)

print('Starting server')
# word2vec = gensim.models.KeyedVectors.load_word2vec_format('models/fil9.vec')

model = fasttext.load_model('models/fil9.bin')
vectors = []

with open('models/fil9.vec') as vec_file:
    next(vec_file)
    j = 0
    for line in vec_file:
        if "'" in line:
            print(line)
        j += 1
        vector = [float(i) for i in line.strip().split(" ")[1:]]
        vectors.append(vector)
print('done loading')


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

    # This is the gensim way to do it, but as far as I can tell, it only accepts words in the vocabulary
    # results = word2vec.most_similar(positive=[word], topn=N)
    # return jsonify([word[0] for word in results])

    word_vec = model[word]
    ban_set = []
    results = []
    for i in range(N):
        nearest_vec_index = fasttext.util.find_nearest_neighbor(
            word_vec, vectors, ban_set)
        results.append(model.words[nearest_vec_index])
        ban_set.append(nearest_vec_index)
    return jsonify(results)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)  # TODO: Grab port from .env file
    print(os.getenv('API_HOST'))
