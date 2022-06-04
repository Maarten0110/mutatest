from abc import ABC, abstractmethod
from typing import List
from replacement_mutator import mutate_by_replacement
from dropout_mutator import mutate_by_dropout


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

    def mutate(self, input_sentence: str, random_seed: int) -> List[str]:
        """
        TODO comment
        """
        return mutate_by_replacement(input_sentence,
                                     num_replacements=self.num_replacements,
                                     num_variants=self.num_variants,
                                     selection_strategy=self.selection_strategy,
                                     random_seed=random_seed)


class DropoutMutator(Mutator):

    def __init__(self,
                 num_dropouts: int = 1):
        """
        TODO comment (get from function)
        """
        self.num_dropouts = num_dropouts

    def mutate(self, input_sentence: str, random_seed: int) -> List[str]:
        # TODO
        return mutate_by_dropout(input_sentence,
                                    num_dropouts=self.num_dropouts,
                                    random_seed=random_seed)