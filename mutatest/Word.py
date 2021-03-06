from typing import Tuple, List, Dict, Iterable
from nltk.corpus import stopwords
import re
from nltk.corpus import wordnet as wn
from nltk.corpus.reader import Synset
from nltk.tokenize import word_tokenize
import nltk

STOPWORDS = stopwords.words('english')
POS_TAG_MAP = {
    'NN': [wn.NOUN],
    'JJ': [wn.ADJ, wn.ADJ_SAT],
    'RB': [wn.ADV],
    'VB': [wn.VERB]
}


class Word:
    """
    A class to represent word that possibly has variants (synonyms/hypernyms) available, as
    suggested by WordNet.

            Attributes
                    value (str):  the actual word

                    pos_tag (str): the WordNet part-of-speech tag as determined by the NLTK
                    package

                    is_stopword (bool): True iff this word is a stopword (as defined by
                    WordNet)

                    variants (Dict[str, int]): variants available for this word. Keys
                    correspond to variants, values to the number of times each variant is suggested
                    by WordNet. (can be interpreted as a measure of variant quality)
    """

    def __init__(self, value: str, pos_tag: str):
        self.value = value.lower()
        self.pos_tag = Word.convert_pos_tag(pos_tag)
        self.is_stopword: bool = value.lower() in STOPWORDS
        self.variants = self._get_variations()

    @property
    def is_nontrivial(self):
        """
        Returns True if and only if this word can be mutated into a different word based on
        hypernym and synonym suggestions by WordNet.
        """
        return not self.is_stopword and not self.pos_tag == '' and not len(self.variants) == 0

    def _get_variations(self) -> Dict[str, int]:
        """
        Uses WordNet to determine variants of this word, where a variant is either a synonym or a
        hypernym.

                Returns:
                    Returns a dictionary which has as its keys the variations available for this
                    word. As its values, the dictionary holds numbers that indicate how many times
                    each variant was suggested by WordNet.
        """
        if self.is_stopword or self.pos_tag == '':
            return dict()

        synsets = wn.synsets(self.value, pos=self.pos_tag)

        synonyms = self._get_synonyms(synsets)
        hypernyms = self._get_hypernyms(synsets)

        result = Word._count_variants(synonyms, hypernyms)

        return result

    def _get_synonyms(self, synsets: List[Synset]) -> List[str]:
        """
        Given the WordNet Synsets available for this word, gather all possible synonyms.
        """
        result: List[str] = []
        for synset in synsets:
            for lemma in synset.lemmas():
                substrings = lemma.name().split('.')
                synonym = substrings[-1]
                synonym_without_underscore = re.sub(r'_', ' ', synonym)
                if self.value != synonym_without_underscore.lower():
                    result.append(synonym_without_underscore)

        return result

    def _get_hypernyms(self, synsets: List[Synset]) -> List[str]:
        """
        Given the WordNet Synsets available for this word, gather all possible hypernyms.
        """
        result: List[str] = []
        for synset in synsets:
            for hypernym in synset.hypernyms():
                for lemma in hypernym.lemmas():
                    substrings = lemma.name().split('.')
                    hypernym = substrings[-1]
                    hypernym_without_underscore = re.sub(r'_', ' ', hypernym)
                    if self.value != hypernym_without_underscore.lower():
                        result.append(hypernym_without_underscore)

        return result

    @staticmethod
    def convert_pos_tag(nltk_pos_tag):
        """
        Converts a NLTK part-of-speech (POS) tag to a WordNet POS tag.
        """
        root_tag = nltk_pos_tag[0:2]
        if root_tag in POS_TAG_MAP.keys():
            return POS_TAG_MAP[root_tag]
        else:
            return ''

    @staticmethod
    def _count_variants(*args: Iterable[str]) -> Dict[str, int]:
        """
        Takes a variable number of string iterables and counts the number of occurrences of each
        unique variant for this Word instance. Result is saved in a dictionary where the keys are
        the unique variants and the values are the number of occurrences of said variant.
        """
        result: Dict[str, int] = dict()

        for variants in args:
            for variant in variants:
                if variant not in result.keys():
                    result[variant] = 1
                else:
                    result[variant] += 1

        return result

    @staticmethod
    def from_tuple(tuple: Tuple[str, str]):
        """
        Creates an instance of ``Word`` from a (token, part-of-speech tag), as generated by the
        functions ``nltk.pos_tag(tokens)``.

                Parameters:
                        ``tuple`` (``Tuple[str, str]``): A tuple with as the first argument the text
                        token, and as its second argument, the tokens POS tag.

                Returns:
                        an instance of ``Word``
        """
        return Word(tuple[0], tuple[1])

    def __repr__(self):
        return f"Word(\"{self.value}\", tag: {self.pos_tag}, stopword: {self.is_stopword})"


def sentence_preprocessing(input_sentence: str) -> List[Word]:
    tokens = word_tokenize(input_sentence)
    tokens_with_pos_tags = nltk.pos_tag(tokens)
    words = [Word.from_tuple(t) for t in tokens_with_pos_tags]

    return words
