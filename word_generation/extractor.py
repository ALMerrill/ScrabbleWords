'''
This script runs through a list of English words in 'en_full.txt' and
counts the number of times each 3 letter combination occurs. It ignores
all words with non-alphabetic characters and words with a count less
than 50 in the dictionary. It saves the results to 'trigram_counts.csv',
where each line is a group of three letters followed by the number of
times that group occured in the dictionary.

'?' as a character represents the starting boundary of a word, and '!'
represents the ending boundary of a word.

Possible improvements:
-Weight the frequency of the trigram by the frequency of the word it comes from
'''

alphabet = 'abcdefghijklmnopqrstuvwxyz'
def is_all_scrabble_chars(word):
    for char in word:
        if not char in alphabet:
            return False
    return True

trigram_counts = {}
with open('en_full.txt') as file:
    text = file.read()
i = 1
lines = text.split('\n')
for line in lines:
    if len(line.split()) < 2:
        break
    word = line.split()[0]
    count = int(line.split()[1])
    if count < 50 or not is_all_scrabble_chars(word.lower()):
        continue
    word = '?' + word + '!'
    for i in range(len(word) - 2):
        trigram = word[i:i+3]
        if not trigram in trigram_counts:
            trigram_counts[trigram] = 0
        trigram_counts[trigram] += 1

print(sorted(trigram_counts, key=trigram_counts.get, reverse=True))

with open('trigram_counts_full.csv', 'w') as out_file:
    for key in trigram_counts.keys():
        print(key, trigram_counts[key], sep=',', file=out_file);
