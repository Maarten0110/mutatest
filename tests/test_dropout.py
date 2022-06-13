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

# We got a huge problem here


def difference_senteces_words(input_tokens, output_sentence):
    from mutatest.Word import sentence_preprocessing

    words = sentence_preprocessing(output_sentence)

    output_tokens = [word.value for word in words]

    return len(list(set(input_tokens) - set(output_tokens)))


def test_dropout():
    from mutatest.mutators import DropoutMutator
    from mutatest.Word import sentence_preprocessing

    TEST_SENTENCES = load_json("tests/resources/example_sentences.json")

    seed(SEED)

    index_1 = randint(0, len(TEST_SENTENCES)-NSENTENCES-1)
    index_2 = index_1+NSENTENCES

    TEST_SENTENCES = TEST_SENTENCES[index_1:index_2]

    TEST_CASES = load_json("tests/resources/test_cases_drop.json")

    counter = 0
    for test_case in TEST_CASES:

        dropout_mutator = DropoutMutator(test_case["num_dropouts"], test_case["num_variants"])

        for test_sentence in TEST_SENTENCES:
            resulting_sentences = dropout_mutator.mutate(test_sentence, SEED, True)
            words = sentence_preprocessing(test_sentence)

            input_tokens = [word.value for word in words]

            if len(resulting_sentences) > 0:
                assert len(
                    resulting_sentences) == test_case["num_variants"], "The dropout mutator is not creating enough variants."
                for result in resulting_sentences:

                    if len(result) > 0:

                        word_difference = difference_senteces_words(
                            input_tokens, result)

                        assert word_difference == test_case["num_dropouts"], "The dropout mutator is not dropping the right amount of words."


test_dropout()
