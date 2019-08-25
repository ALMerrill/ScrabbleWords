from markovchain import JsonStorage
from markovchain.text import MarkovText, ReplyMode

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

    # markov.save('markov.json')

    # we can actually save the full definition model into a json file to make that part quicker
    # markov = MarkovText.from_file('markov.json')


def markovify_example():
    with open('word_generation/definitions.txt') as f:
        text = f.read()

    neighbor_model = markovify.Text(text)
    # full_definition_model = markovify.Text(all_definitions)

    # You can combine the model with the neighbor defintions with a model with a ton of definitons
    # and weight it towards the neighbors to get something more like those definitions. (not tested
    # because I don't have that other text file)
    # combined_model = markovify.combine([neighbor_model, full_definition_model], [3, 1])

    print(neighbor_model.make_sentence() + '\n')
    print(neighbor_model.make_short_sentence(280) + '\n')
    # print(combined_model.make_sentence())


if __name__ == "__main__":
    markovchain_example()
    markovify_example()
