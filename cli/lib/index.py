import os
import pickle
from collections import Counter, defaultdict

from .common import tokens
from .load_content import CACHE_DIR, load_content


class InvertedIndex:
    def __init__(self) -> None:
        self.index = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
        self.term_frequency_path = os.path.join(CACHE_DIR, "term_frequencies.pkl")
        self.term_frequencies = defaultdict(Counter)

    def __add_documents(self, doc_id, text) -> None:
        tokenize_text = tokens(text)
        self.term_frequencies[doc_id] = Counter(tokenize_text)
        for token in tokenize_text:
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list:
        return list(self.index[term.lower()])

    def get_tf(self, doc_id: int, term: str) -> int:
        tokenize_text = tokens(term)
        if len(tokenize_text) > 1:
            raise ValueError("Term should only contain one token")
        return self.term_frequencies[doc_id][tokenize_text[0]]

    def build(self):
        movies = load_content()
        for index, movie in enumerate(movies, start=1):
            self.__add_documents(movie['id'], f"{movie['title']} {movie['description']}")
            self.docmap[index] = movie

    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)
        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)
        with open(self.term_frequency_path, "wb") as f:
            pickle.dump(self.term_frequencies, f)

    def load(self):
        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)
        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)
        with open(self.term_frequency_path, "rb") as f:
            self.term_frequencies = pickle.load(f)


def build_indexes():
    index = InvertedIndex()
    index.build()
    index.save()


def get_term_frequencies(doc_id: int, term: str):
    index = InvertedIndex()
    index.load()

    frequencies = index.get_tf(doc_id, term)
    print(f"ID: {doc_id} - Term: {term} - Frequency: {frequencies}")
