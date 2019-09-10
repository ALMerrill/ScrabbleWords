import difflib
import enchant

dictionary = enchant.Dict("en_US")
all_words = []

alphabet = 'abcdefghijklmnopqrstuvwxyz'
def is_all_scrabble_chars(word):
    for char in word:
        if not char in alphabet:
            return False
    return True

def init():
    with open('../word_generation/en_full.txt') as word_file:
        lines = word_file.readlines()
    for line in lines:
        if len(line.split()) < 2:
            break
        word, count = line.split()
        if is_all_scrabble_chars(word.lower()) and dictionary.check(word):
            all_words.append(word)


def get_nearest_neighbors(word):
    if not all_words:
        init()
    return difflib.get_close_matches(word, all_words, n=4, cutoff=0.3) #, cutoff=0.6


# # Uncomment this to test in console
# while True:
#     print(get_nearest_neighbors(input('Enter a word: ')))
