import fasttext
import fasttext.util
import gensim
import nltk
from nltk.corpus import wordnet as wn
from . import word_getter
from . import edit_distance

nltk.download('wordnet')


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


def nearest_neighbors(model, word, vectors):
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
    num_tries = 3
    N = 50
    for _ in range(num_tries):
        nearest_vec_index = fasttext.util.find_nearest_neighbor(
            word_vec, vectors, ban_set)
        neighbor_word = model.words[nearest_vec_index]
        print(neighbor_word)
        print(word_getter.check(neighbor_word))
        isWord = word_getter.check(neighbor_word)
        if isWord:
            results.append(neighbor_word)
        ban_set.append(nearest_vec_index)
    remaining = N - len(results)
    if remaining > 0:
        i = 0
        while len(results) < N:
            results.extend(
                edit_distance.get_nearest_neighbors(word, remaining + i))
            i += 1
            results = list(set(results))
    return results


def nearest_neighbor_gensim(model, word, N):
    # This is the gensim way to do it, but the con is that it only accepts words that are in the vocabulary
    results = model.most_similar(positive=[word], topn=N)
    return [word[0] for word in results]


def get_definitions(wordList):
    """Looks up the defintions of each word in wordList and returns a list of their definitions

    Arguments:
        wordList [string list] - a list of words
    Return:
        definitions [map<string, string>] - a map from words to their definitions
    """
    # Note: each synset is a list of words with similiar definitions.
    # So, right now it adds all of the definitions for all words in the synsets.
    # Usually, the synsets just contain the same word but different defintions.
    # Occasionally they have synonyms that are different words.
    definitions = ""
    for word in wordList:
        for synset in wn.synsets(word):
            definition += "%s\n" % synset.definition()
    return definitions


# model, vectors = load_model('fil9.vec')
# while True:
#     print(nearest_neighbors(model, input('Enter a word: '), vectors))
