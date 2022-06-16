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

    words_sentence1 = word_tokenize(sentence1.lower().strip())
    words_sentence2 = word_tokenize(sentence2.lower().strip())

    result = 0
    counter = 0
    for word in words_sentence1:

        if word != words_sentence2[counter]:
            result += 1
        counter += 1

    return result


def test_replacement():
    from mutatest.mutators import ReplacementMutator, text_prepare

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

            test_sentence = text_prepare(test_sentence)

            resulting_sentences = replacement_mutator.mutate(test_sentence, SEED, True)
            if resulting_sentences != []:

                assert len(
                    resulting_sentences) == test_case["num_variants"], "The replacement mutator is not creating enough variants."

            for result in resulting_sentences:
                if len(result) > 0:

                    if difference_senteces_words(
                            test_sentence, result) != test_case["num_replacements"]:

                        print("difference", difference_senteces_words(
                            test_sentence, result))
                        print("Needed: ", test_case["num_replacements"])

                        print("test sentence: ", word_tokenize(test_sentence))
                        print("result: ", word_tokenize(result))

                    # assert difference_senteces_words(
                    #     test_sentence, result) == test_case["num_replacements"], "The replacement mutator is not changing the right amount of words."


test_replacement()
