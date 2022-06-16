# Mutatest

Mutamorphic-test is a python3 package that provides of a two different kinds of word mutators for sentences, meaning that the original sentence will be transformed by this mutators.

## How to install it

In order to install the latest version use the python3 installer pip3.

```bash
pip3 install mutamorphic-test 
```

## How to use it

In order to use the package we need to import the mutators first with the statement:

```python
from mutatest.mutators import ReplacementMutator,DopoutMutator
```

Once we have them imported we can use them. We have to create an instance of the classes in order to use them.

We can specify how many words we want them to modify, how many variants of the sentence shall be created and, in the case of the replacement, which strategy shall be used to select the words to be changed.


For the two mutators we need the following parameters (we can also use the default values):

```python
ReplacementMutator(num_replacements: int = 1, num_variants: int = 5, selection_strategy: str = "random")
DropoutMutator(num_dropouts: int = 1, num_variants: int = 1)
```

Once we have our mutator we can perform mutation on a sentence in the following way:

```python
mutated_sentence=mutator.mutate(sentence,random_seed=42)
```

A full example of how this package can be used would be the following:


```python
from mutatest.mutators import ReplacementMutator

mutator=ReplacementMutator()
sentence="This is an example sentence"

mutated_sentence=mutator.mutate(sentence,random_seed=42)

print(mutated_sentence)

```
