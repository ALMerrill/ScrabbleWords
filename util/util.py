import fasttext
import fasttext.util
import gensim


def load_model(filename):
    model = fasttext.load_model('models/fil9.bin')
    vectors = []

    with open('models/' + filename) as f:
        next(f)
        lines = f.readlines()
    vectors = [[float(i) for i in line.strip().split(" ")[1:]]
               for line in lines]
    return model, vectors


def load_gensim_model(filename):
    word2vec = gensim.models.KeyedVectors.load_word2vec_format(
        'models/' + filename)


def nearest_neighbor(model, word, vectors, N):
    word_vec = model[word]
    ban_set = []
    results = []
    for i in range(N):
        nearest_vec_index = fasttext.util.find_nearest_neighbor(
            word_vec, vectors, ban_set)
        results.append(model.words[nearest_vec_index])
        ban_set.append(nearest_vec_index)
    return results


def nearest_neighbor_gensim(model, word, N):
    # This is the gensim way to do it, but the con is that it only accepts words that are in the vocabulary
    results = model.most_similar(positive=[word], topn=N)
    return [word[0] for word in results]
