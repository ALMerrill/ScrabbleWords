from markovchain import JsonStorage
from markovchain.text import MarkovText, ReplyMode
import json

import markovify


def markovchain_example():
    markov = MarkovText()

    with open('word_generation/definitions.txt') as fp:
        for line in fp:
            markov.data(line, part=True)
    markov.data('', part=False)

    print(markov(max_length=16) + '\n')
    print(markov(max_length=16, reply_to='sentence start',
                 reply_mode=ReplyMode.END) + '\n')


def markovify_example():
    with open('word_generation/definitions.txt') as f:
        text = f.read()

    neighbor_model = markovify.Text(text)

    print(neighbor_model.make_sentence() + '\n')
    print(neighbor_model.make_short_sentence(280) + '\n')


def convert_json_to_txt():
    with open('word_generation/dictionary.json') as f_in:
        dict_text = json.load(f_in)
    with open('word_generation/dictionary.txt', 'w+') as f_out:
        for word in dict_text:
            f_out.write(dict_text[word] + '\n')


def make_model():
    with open('word_generation/dictionary_model.json') as f:
        dictionary_model_json = json.load(f)
        dictionary_model = markovify.Text.from_json(dictionary_model_json)

    with open('word_generation/definitions.txt') as f:
        definitions = f.read()
    neighbor_model = markovify.Text(definitions, well_formed=False)

    # Combined model weighted 1 to 3 towards the neighbor_model to be more like the neighbor definitions
    combined_model = markovify.combine(
        [dictionary_model, neighbor_model], [1, 3])
    for _ in range(5):
        print(combined_model.make_sentence() + '\n')


def create_dictionary_model():
    with open('word_generation/dictionary.txt') as f:
        dictionary = f.read()

    dictionary_model = markovify.Text(dictionary)

    dictionary_model_json = dictionary_model.to_json()
    with open('word_generation/dictionary_model.json', 'w', encoding='utf-8') as f:
        json.dump(dictionary_model_json, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    make_model()
    # markovchain_example()
    # markovify_example()
