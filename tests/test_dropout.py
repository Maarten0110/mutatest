import sys
import json
from nltk.tokenize import word_tokenize
import os
from random import randint, seed
sys.path.insert(0, os.getcwd()+"/mutatest")
sys.path.insert(0, os.getcwd())

NSENTENCES = 100
SEED = 420


def load_json(filename):
    with open(filename, "r") as file:
        return json.load(file)


def difference_senteces_words(sentence1, sentence2):

    words_sentence1 = word_tokenize(sentence1)
    words_sentence2 = word_tokenize(sentence2)

    return len(list(set(words_sentence1) - set(words_sentence2)) + list(set(words_sentence2) - set(words_sentence1)))


def test_dropout():
    from mutatest.mutators import DropoutMutator

    TEST_SENTENCES = load_json("tests/resources/example_sentences.json")

    seed(SEED)

    index_1 = randint(0, len(TEST_SENTENCES)-NSENTENCES-1)
    index_2 = index_1+NSENTENCES

    TEST_SENTENCES = TEST_SENTENCES[index_1:index_2]

    TEST_CASES = load_json("tests/resources/test_cases_drop.json")

    for test_case in TEST_CASES:

        dropout_mutator = DropoutMutator(test_case["num_dropouts"], test_case["num_variants"])

        for test_sentence in TEST_SENTENCES:
            resulting_sentences = dropout_mutator.mutate(test_sentence, SEED, True)
            for result in resulting_sentences:
                if len(result) > 0:

                    assert len(
                        resulting_sentences) == test_case["num_variants"], "The dropout mutator is not creating enough variants."
                    assert difference_senteces_words(
                        test_sentence, result), "The dropout mutator is not dropping enough words."

        # print(dropout_mutator.non_mutated)


test_dropout()
