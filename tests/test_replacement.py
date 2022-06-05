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


def test_replacement():
    from mutatest.mutators import ReplacementMutator

    TEST_SENTENCES = load_json("tests/resources/example_sentences.json")

    seed(SEED)

    index_1 = randint(0, len(TEST_SENTENCES)-NSENTENCES-1)
    index_2 = index_1+NSENTENCES

    TEST_SENTENCES = TEST_SENTENCES[index_1:index_2]

    TEST_CASES = load_json("tests/resources/test_cases_replacement.json")

    for test_case in TEST_CASES:

        replacement_mutator = ReplacementMutator(
            num_replacements=test_case["num_replacements"], num_variants=test_case["num_variants"], selection_strategy=test_case["selection_strategy"])

        for test_sentence in TEST_SENTENCES:
            resulting_sentences = replacement_mutator.mutate(test_sentence, SEED, True)
            for result in resulting_sentences:
                if len(result) > 0:

                    assert len(
                        resulting_sentences) == test_case["num_variants"], "The replacement mutator is not creating enough variants."
                    assert difference_senteces_words(
                        test_sentence, result), "The replacement mutator is not replacing enough words."

        # print(replacement_mutator.non_mutated)


test_replacement()
