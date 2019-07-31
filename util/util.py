import fasttext
import fasttext.util
import gensim
import enchant


dictionary = enchant.Dict("en_US")


def load_model(filename):
    """loads a fasttext model from the given filename
    Arguments:
        filename [string] - The name of the .bin file containing the model
    Returns:
        [fasttext model]
    """
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
    """ Given a word, return the N nearest neighbors
    Arguments:
        model [fasttext model] - loaded from a .bin file
        word [string] - the word for which to find the nearest neighbors
        vectors [list] - of the vectors to compare to to find neighbors
        N [int] - the number of neighbors to find
    Returns:
        [list of strings] - the N nearest neighbors
    """
    word_vec = model[word]
    ban_set = []
    results = []
    while len(results) < N:
        nearest_vec_index = fasttext.util.find_nearest_neighbor(
            word_vec, vectors, ban_set)
        neighbor_word = model.words[nearest_vec_index]
        print(neighbor_word)
        print(dictionary.check(neighbor_word))
        isWord = dictionary.check(neighbor_word)
        if isWord:
            results.append(neighbor_word)
        ban_set.append(nearest_vec_index)
    return results


def nearest_neighbor_gensim(model, word, N):
    # This is the gensim way to do it, but the con is that it only accepts words that are in the vocabulary
    results = model.most_similar(positive=[word], topn=N)
    return [word[0] for word in results]
