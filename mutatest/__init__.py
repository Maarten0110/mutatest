import nltk

__all__ = [
    "dropout_mutator",
    "mutators",
    "replacement_mutator",
    "test_runner",
    "Word",
]

nltk.download('wordnet')
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('omw-1.4')
