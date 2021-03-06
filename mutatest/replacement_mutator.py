from typing import Tuple, List, Callable
from .Word import Word, sentence_preprocessing

import random as random_pkg
from random import Random


def _select_mutations_random(non_trivial_words: List[Word],
                             num_replacements: int,
                             num_variants: int,
                             rng: Random,
                             assure_variants: bool = False) -> List[List[Tuple[Word, str]]]:
    """
    Selects mutations at random. Ensures that each output sentence is unique, although mutations
    at the nontrivial word level might be reused across output sentences. For each output sentence,
    words are selected randomly, without replacement, to be mutated. Then, for the selected words,
    a variant (synonym/hypernym) is chosen at random (uniform dist.) from the available variants of
    that word.

            Parameters:
                ``nontrivial_words`` (``List[Word]``): a list of all nontrivial words (words that
                can be replaced by a variant (synonym/hypernym)

                ``num_replacements`` (``int``): the number of words that should be replaced per
                output sentence

                ``num_variants`` (``int``): the number of output sentences

                ``rng`` (``Random``): the random generator instance used to make random choices

            Returns:
                A list of mutations to be made for each output sentence. For each output sentence,
                the function returns a list of tuples representing the mutation. The first element
                of the tuple is the nontrivial word that is to be replaced. The second element of
                the tuple is the variant that was chosen for the word as a replacement.
    """
    # If we want to assure the number of variants we do not use the phrase
    # Otherwise we return as many variants as possible.
    if num_replacements > len(non_trivial_words):

        if assure_variants:
            return []
        else:
            num_replacements = len(non_trivial_words)

    choices = set()

    # This counter is for the case where there are not enough variants for the words.
    safety_counter = 0
    safety_limit = 500
    for _ in range(num_variants):

        while True:
            words = rng.sample(non_trivial_words, num_replacements)

            mutations = {(word, rng.choice(list(word.variants.keys()))) for word in words}

            mutations = frozenset(mutations)

            if safety_counter == safety_limit:
                return list()

            if mutations not in choices:
                choices.add(mutations)
                break
            else:
                safety_counter += 1

    mutations_list = [list(mutations) for mutations in choices]

    return mutations_list


def _select_mutations_most_common_first(nontrivial_words: List[Word],
                                        num_replacements: int,
                                        num_variants: int,
                                        rng: Random,
                                        assure_variants: bool = False) -> List[List[Tuple[Word, str]]]:
    """
    Selects mutations based on how many times a variant for a nontrivial word was suggested by
    WordNet. The mutations with the highest counts are chosen first. But for a single word, only one
    mutation is chosen at a time. So if for a sentence, a mutation is chosen for word X, when more
    mutations still need to be chosen, the mutation with the highest count for word Y is chosen,
    where X =/= Y. If variants with equal counts are considered, a uniformly random choice is made.

            Parameters:
                ``nontrivial_words`` (``List[Word]``): a list of all nontrivial words (words that
                can be replaced by a variant (synonym/hypernym)

                ``num_replacements`` (``int``): the number of words that should be replaced per
                output sentence

                ``num_variants`` (``int``): the number of output sentences

                ``rng`` (``Random``): the random generator instance used to make random choices

            Returns:
                A list of mutations to be made for each output sentence. For each output sentence,
                the function returns a list of tuples representing the mutation. The first element
                of the tuple is the nontrivial word that is to be replaced. The second element of
                the tuple is the variant that was chosen for the word as a replacement.
    """

    # Some preparations: group mutations by the number of times it is suggested by WordNet

    grouped_by_counts = {}
    used_words = []
    for word in nontrivial_words:

        for variant, count in word.variants.items():
            if word.value not in used_words:
                used_words.append(word.value)
            if count not in grouped_by_counts.keys():
                grouped_by_counts[count] = {(word, variant)}
            else:
                grouped_by_counts[count].add((word, variant))

    if len(nontrivial_words) < num_replacements or len(used_words) < num_replacements:
        return []
    groups = list(grouped_by_counts.keys())

    groups.sort(reverse=True)

    # Choose the mutations.
    mutations_list = []
    for _ in range(num_variants):

        mutations = []
        chosen_words = set()
        current_group_number = 0

        while len(chosen_words) < num_replacements and current_group_number < len(groups):

            group = grouped_by_counts[groups[current_group_number]]

            # We do not want single words to be replaced by two wrods
            candidates = [x for x in group if x[0] not in chosen_words]

            if len(candidates) > 0:

                mutation = rng.choice(candidates)
                chosen_words.add(mutation[0])

                mutations.append(mutation)

                group.remove(mutation)
            else:
                current_group_number += 1
        if current_group_number == len(groups):
            # If we do not get all the variants we want we return an empty list
            # Or we just return the results so far, if is not strict.
            if assure_variants:
                return list()
            else:
                break

        mutations_list.append(mutations)

    return mutations_list


MUTATION_SELECTION_STRATEGIES = {
    "random": _select_mutations_random,
    "most_common_first": _select_mutations_most_common_first,
}


def _get_selection_strategy_func(selection_strategy: str) \
        -> Callable[[List[Word], int, int, Random], List[List[Tuple[Word, str]]]]:
    """
    A basic dictionary lookup to select either of the two mutation selection strategies.
    """

    assert selection_strategy in MUTATION_SELECTION_STRATEGIES, \
        "Unknown mutation selection strategy."

    return MUTATION_SELECTION_STRATEGIES[selection_strategy]


def mutate_by_replacement(input_sentence: str,
                          num_replacements: int = 1,
                          num_variants: int = 5,
                          selection_strategy: str = "random",
                          random_seed: int = 13,
                          assure_variants: bool = False) -> List[str]:
    """
    Returns a list of mutated version of the given input sentence. Mutations are based on synonyms
    and hypernyms of nontrivial words. Nontrivial words are words that are not stopwords (as defined
    by WordNet and have at least one synonym/hypernym available. The synonyms/hypernyms are based on
    WordNet Synsets.

    WordNet suggests a lot of variants (synonyms or hypernyms) for each nontrivial word. The same
    variant can be suggested multiple times in different Synsets. This can be taken as a measure of
    'variant quality'. There are two strategies available for choosing variants as mutations:

    1) "random": each variant has an equal chance of being chosen, regardless of how many times it
    was suggested by WordNet.
    2) "most_common_first": variants that were suggested often are chosen first.

            Parameters:
                ``input_sentence`` (``str``): the input sentence

                ``num_replacements`` (``int``): the number of words that should be replaced per
                output sentence

                ``num_variants`` (``int``): the number of output sentences

                ``selection_strategy`` (``str``): the desired selection mutation strategy, which can
                be either "random" (default) or "most_common_first"

                ``random_seed`` (``int``):

            Returns:
                A list mutated sentences.
    """
    # Set thread safe seed for reproducibility
    rng = random_pkg.Random()
    rng.seed(a=random_seed)

    words = sentence_preprocessing(input_sentence)

    non_trivial_words = {word: index for (index, word) in enumerate(words) if word.is_nontrivial}

    selection_strategy_func = _get_selection_strategy_func(selection_strategy)

    mutations_list = selection_strategy_func(list(non_trivial_words.keys()),
                                             num_replacements,
                                             num_variants,
                                             rng, assure_variants)

    mutated_sentences = []
    sentence_og = [word.value for word in words]

    for mutations in mutations_list:
        sentence = sentence_og.copy()
        for mutation in mutations:
            word = mutation[0]

            # In order to avoid words that are substitued by two words
            replacement = mutation[1].replace(" ", "-")

            # Not ideal but nothing more makes sense
            if replacement == '':
                replacement = "-"+word.value+"-"

            index = non_trivial_words[word]
            sentence[index] = replacement

        mutated_sentence = " ".join(sentence)
        mutated_sentences.append(mutated_sentence)

    return mutated_sentences


if __name__ == "__main__":
    test_sentence = "Uploading files via JSON Post request to a Web Service provided by Teambox"
    result = mutate_by_replacement(test_sentence,
                                   num_replacements=2,
                                   num_variants=10,
                                   selection_strategy="most_common_first")
    print(f"ORIGINAL: \n{test_sentence}")
    print("VARIANTS:")
    for x in result:
        print(x)
