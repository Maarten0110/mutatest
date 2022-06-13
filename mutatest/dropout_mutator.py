from typing import Tuple, List, Callable
from .Word import Word
from nltk.tokenize import word_tokenize
import nltk
import random as random_pkg
from random import Random
from itertools import combinations


def mutate_by_dropout(input_sentence: str,
                      num_dropouts: int = 1,
                      random_seed: int = 13,
                      num_variants: int = 100,
                      assure_variants: bool = False) -> List[str]:
    """
    Returns a list of mutated version of the given input sentence by removing some important words.

            Parameters:
                ``input_sentence`` (``str``): the input sentence

                ``num_dropouts`` (``int``): the number of words that should be dropped out per
                output sentence

                ``random_seed`` (``int``):

            Returns:
                A list mutated sentences.
    """
    # Set thread safe seed for reproducibility
    rng = random_pkg.Random()
    rng.seed(a=random_seed)

    tokens = word_tokenize(input_sentence)
    tokens_with_pos_tags = nltk.pos_tag(tokens)
    words = [Word.from_tuple(t) for t in tokens_with_pos_tags]
    non_stopword_list = {word.value for word in words if not word.is_stopword}
    mutated_sentences = []
    for subset in combinations(non_stopword_list, num_dropouts):
        sentence = [word.value for word in words]
        for remove_word in subset:
            sentence.remove(remove_word)
        mutated_sentences.append(" ".join(sentence))
        if len(mutated_sentences) == num_variants:
            break

    # This is mostly used for testing, to assure the number of variants
    if len(mutated_sentences) < num_variants and assure_variants:
        return list()

    return mutated_sentences


if __name__ == "__main__":
    test_sentence = "Uploading files via JSON Post request to a Web Service provided by Teambox"
    result = mutate_by_dropout(test_sentence,
                               num_dropouts=2)
    print(f"ORIGINAL: \n{test_sentence}")
    print("VARIANTS:")
    for x in result:
        print(x)
