with open('../all_valid_words.txt') as words_file:
    all_words = set(words_file.read().splitlines())


def get_all_words():
    return list(all_words)

def check(word):
    return word in all_words
