from abc import ABC, abstractmethod
from typing import List
from .dropout_mutator import mutate_by_dropout
from .replacement_mutator import mutate_by_replacement
from nltk.tokenize import word_tokenize
from .Word import Word
import re
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')


def text_prepare(text):
    """
        text: a string
        return: modified initial string
    """
    REPLACE_BY_SPACE_RE = re.compile('[/(){}\[\]\|@,;]')
    BAD_SYMBOLS_RE = re.compile('[^0-9a-z #+_]')
    STOPWORDS = set(stopwords.words('english'))

    text = text.lower()  # lowercase text
    text = re.sub(REPLACE_BY_SPACE_RE, " ", text)  # replace REPLACE_BY_SPACE_RE symbols by space in text
    text = re.sub(BAD_SYMBOLS_RE, "", text)  # delete symbols which are in BAD_SYMBOLS_RE from text
    text = " ".join([word for word in text.split() if not word in STOPWORDS])  # delete stopwords from text
    return text


class Mutator(ABC):
    """
    TODO comment
    """

    @abstractmethod
    def mutate(self, input_sentence: str, random_seed: int) -> List[str]:
        """
        TODO comment
        """
        raise NotImplementedError()

# Both checks that I putted are kind of crap


class ReplacementMutator(Mutator):

    def __init__(self,
                 num_replacements: int = 1,
                 num_variants: int = 5,
                 selection_strategy: str = "random"):
        """
        TODO comment (get from function)
        """
        self.num_replacements = num_replacements
        self.num_variants = num_variants
        self.selection_strategy = selection_strategy
        self.non_mutated = 0

    def mutate(self, input_sentence: str, random_seed: int, assure_variants: bool = False) -> List[str]:
        """
        TODO comment
        """
        results = mutate_by_replacement(input_sentence,
                                        num_replacements=self.num_replacements,
                                        num_variants=self.num_variants,
                                        selection_strategy=self.selection_strategy,
                                        random_seed=random_seed,
                                        assure_variants=assure_variants)

        if len(results) == 0:
            self.non_mutated += 1

        return results


class DropoutMutator(Mutator):

    def __init__(self,
                 num_dropouts: int = 1, num_variants: int = 1):
        """
        TODO comment (get from function)
        """
        self.num_dropouts = num_dropouts
        self.num_variants = num_variants
        self.non_mutated = 0

    def mutate(self, input_sentence: str, random_seed: int = 13, assure_variants: bool = False) -> List[str]:

        results = mutate_by_dropout(input_sentence,
                                    num_dropouts=self.num_dropouts,
                                    random_seed=random_seed,
                                    num_variants=self.num_variants,
                                    assure_variants=assure_variants)

        if len(results) == 0:
            self.non_mutated += 1

        return results
