import difflib
from . import word_getter

all_words = []

alphabet = 'abcdefghijklmnopqrstuvwxyz'


def is_all_scrabble_chars(word):
    for char in word:
        if not char in alphabet:
            return False
    return True


def init():
    global all_words
    all_words = word_getter.get_all_words()


def get_nearest_neighbors(word, N):
    if not all_words:
        init()
    # , cutoff=0.6
    return difflib.get_close_matches(word, all_words, n=N, cutoff=0.3)


# # Uncomment this to test in console
# while True:
#     print(get_nearest_neighbors(input('Enter a word: ')))
