from abc import ABC, abstractmethod
from typing import List
from .dropout_mutator import mutate_by_dropout
from .replacement_mutator import mutate_by_replacement


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
        # TODO
        results = mutate_by_dropout(input_sentence,
                                    num_dropouts=self.num_dropouts,
                                    random_seed=random_seed,
                                    num_variants=self.num_variants,
                                    assure_variants=assure_variants)
        if len(results) == 0:
            self.non_mutated += 1

        return results
