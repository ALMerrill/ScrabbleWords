'''
This script reads the trigram counts from 'trigram_counts_full.txt'.
Using those counts, given a random group of up to MAX_LENGTH letters,
it will come up with which ordering of letters is the most likely to
actually be a word.

Possible improvements:
-Try other ways of calculating the probability rather than just summing
the trigram frequencies
-If a combination actually appears in the dictionary, return that one instead of
making one up.
'''

trigram_counts = {}
initiated = False
MAX_LENGTH = 7

def init():
    with open ('trigram_counts_full.csv') as file:
        lines = file.readlines()
    for line in lines:
        if len(line.split(',')) < 2:
            break
        trigram, count = line.split(',')
        trigram_counts[trigram] = int(count)
    initiated = True

def get_combinations(word, remaining_letters):
    if len(word) >= MAX_LENGTH:
        return [word]
    if len(remaining_letters) == 1:
        return [word + remaining_letters]
    combinations = []
    if len(word) >= 3:
        combinations = [word]
    for i in range(len(remaining_letters)):
        combinations += get_combinations(word + remaining_letters[i], remaining_letters[:i] + remaining_letters[i+1:])
    return combinations

def generate(letters):
    if len(letters) > MAX_LENGTH:
        print('Cannot predict for that many letters! (max of {MAX_LENGTH})')
        return
    if not initiated:
        init()
    all_combinations = get_combinations('', letters)
    best_score = 0
    best_word = ''
    for combination in all_combinations:
        formalized_word = '?' + combination + '!'
        score = 0
        for i in range(len(formalized_word) - 2):
            trigram = formalized_word[i:i+3]
            if trigram in trigram_counts:
                score += trigram_counts[trigram]
        if score > best_score:
            best_word = combination
            best_score = score
    return best_word

# # Use this to test it in a console. It's kinda fun!
# while True:
#     letters = input('What letters do you want to guess? ')
#     print(generate(letters))
