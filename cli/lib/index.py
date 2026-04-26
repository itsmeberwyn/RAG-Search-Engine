import os
import pickle
from collections import defaultdict

from .common import tokens
from .load_content import CACHE_DIR, load_content


class InvertedIndex:
    def __init__(self) -> None:
        self.index = defaultdict(set)
        self.docmap: dict[int, dict] = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")

    def __add_documents(self, doc_id, text) -> None:
        tokenize_text = tokens(text)
        for token in tokenize_text:
            self.index[token].add(doc_id)

    def get_documents(self, term: str) -> list:
        return list(self.index[term.lower()])

    def build(self):
        movies = load_content()
        for index, movie in enumerate(movies, start=1):
            self.__add_documents(index, f"{movie['title']} {movie['description']}")
            self.docmap[index] = movie

    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(self.index_path, "wb") as f:
            pickle.dump(self.index, f)
        with open(self.docmap_path, "wb") as f:
            pickle.dump(self.docmap, f)

    def load(self):
        with open(self.index_path, "rb") as f:
            self.index = pickle.load(f)
        with open(self.docmap_path, "rb") as f:
            self.docmap = pickle.load(f)


def build_indexes():
    index = InvertedIndex()
    index.build()
    index.save()
