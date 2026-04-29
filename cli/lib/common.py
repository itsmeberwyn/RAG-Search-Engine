import string

from nltk.stem import PorterStemmer

from .load_content import load_stopwords

stemmer = PorterStemmer()


def translate_text(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))


def tokenize_text(text: str) -> list[str]:
    return text.lower().split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopwords = load_stopwords()
    set_tokens = tokens
    return [token for token in set_tokens if token not in stopwords]


def stem_keywords(token: str) -> str:
    return stemmer.stem(token)


def format_search_result(results: list[dict]):
    print("Searching for: QUERY")
    for index, result in enumerate(results, start=1):
        print(f"{index + 1}. ({result['id']}) {result['title']}")


def tokens(text: str) -> list[str]:
    normalize = translate_text(text)
    tokenize = tokenize_text(normalize)
    filtered_tokens = remove_stopwords(tokenize)

    stemmed_words = []
    for word in filtered_tokens:
        stemmed_words.append(stem_keywords(word))
    return stemmed_words
