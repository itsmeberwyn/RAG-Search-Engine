import argparse
import json
import string
from pathlib import Path

from nltk.stem import PorterStemmer

stemmer = PorterStemmer()


def load_content() -> list[str]:
    curr_dir = Path(__file__).parent
    movies_path = curr_dir / "../data/movies.json"
    content = []

    with open(movies_path) as f:
        content = json.load(f)
    return content["movies"]


def load_stopwords() -> list[str]:
    curr_dir = Path(__file__).parent
    movies_path = curr_dir / "../data/stopwords.txt"
    content = []

    with open(movies_path, "r") as f:
        content = f.read().splitlines()
    return content


def search(query, movies, limit=5) -> list[dict]:
    results = []
    seen = set()
    for movie in movies:
        title = movie["title"]
        search_query = query
        translator = str.maketrans("", "", string.punctuation)

        normalize_title = title.translate(translator)
        normalize_query = search_query.translate(translator)

        tokenize_title = tokenize_text(normalize_title)
        tokenize_query = tokenize_text(normalize_query)

        clean_title = remove_stopwords(tokenize_title)
        clean_query = remove_stopwords(tokenize_query)

        for query_token in clean_query:
            for title_token in clean_title:
                movie_id = movie["id"]
                if movie_id not in seen and stem_keywords(query_token) in stem_keywords(title_token):
                    seen.add(movie_id)
                    results.append(movie)
    sorted_items = sorted(results, key=lambda x: x["id"])
    return sorted_items[:limit]


def format_search_result(results: list[dict]):
    print("Searching for: QUERY")
    for index, result in enumerate(results):
        print(f"{index + 1}. {result['title']}")


def tokenize_text(text: str) -> list[str]:
    return text.lower().split()


def remove_stopwords(tokens: list[str]) -> list[str]:
    stopwords = load_stopwords()
    set_tokens = set(tokens)
    return [token for token in set_tokens if token not in stopwords]


def stem_keywords(token: str) -> str:
    return stemmer.stem(token)


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            movies = load_content()
            results = search(args.query, movies)
            format_search_result(results)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
