from nltk.stem import PorterStemmer

from .load_content import load_stopwords

stemmer = PorterStemmer()


def tokenize_text(text: str) -> list[str]:
    return text.lower().split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopwords = load_stopwords()
    set_tokens = set(tokens)
    return [token for token in set_tokens if token not in stopwords]


def stem_keywords(token: str) -> str:
    return stemmer.stem(token)


def format_search_result(results: list[dict]):
    print("Searching for: QUERY")
    for index, result in enumerate(results):
        print(f"{index + 1}. {result['title']}")
