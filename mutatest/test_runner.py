from typing import List, Iterable, Callable, Generic, TypeVar
from .mutators import Mutator
import numpy as np

ModelOutput = TypeVar("ModelOutput")


class MutamorphicTestCase(Generic[ModelOutput]):
    """
    TODO comment
    """

    def __init__(self, input_sentence: str):
        self.input_sentence = input_sentence
        self.variants: List[str] | None = None
        self.output_original: ModelOutput | None = None
        self.output_variants: List[ModelOutput] | None = None
        self.similarities: List[float] = []

    def compute_variants(self, mutator: Mutator, random_seed: int):
        """
        TODO comment
        """
        self.variants = mutator.mutate(self.input_sentence, random_seed=random_seed)

    def compute_model_outputs(self, model_callback: Callable[[str], ModelOutput]):
        """
        TODO comment
        """
        assert self.variants is not None, "Make sure to run compute_variants() before this."

        self.output_original = model_callback(self.input_sentence)
        self.output_variants = [model_callback(x) for x in self.variants]

    def compute_similarities(self,
                             similarity_callback: Callable[[ModelOutput, ModelOutput], float]):
        """
        TODO comment
        """
        assert self.output_original is not None and self.output_variants is not None, \
            "Make sure to run compute_model_outputs() before this."

        self.similarities = [similarity_callback(self.output_original, x)
                             for x in self.output_variants]

    @property
    def average_similarity(self) -> float:
        return np.average(self.similarities)


class MutamorphicTest(Generic[ModelOutput]):
    """
    TODO comment
    """

    def __init__(self,
                 input_sentences: Iterable[str],
                 mutator: Mutator,
                 model_callback: Callable[[str], ModelOutput],
                 similarity_callback: Callable[[ModelOutput, ModelOutput], float],
                 random_seed: int = 13):
        """
        TODO comment
        """
        self.test_cases = [MutamorphicTestCase(x) for x in input_sentences]
        self.mutator = mutator
        self.model_callback = model_callback
        self.similarity_callback = similarity_callback
        self.random_seed = random_seed

    def run(self):
        """
        TODO comment
        """
        for test_case in self.test_cases:
            test_case.compute_variants(mutator=self.mutator, random_seed=self.random_seed)
            test_case.compute_model_outputs(self.model_callback)
            test_case.compute_similarities(self.similarity_callback)

    @property
    def average_similarity(self) -> float:
        return np.average([x.average_similarity for x in self.test_cases])
