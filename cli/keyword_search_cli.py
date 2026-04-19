import argparse

from lib.common import format_search_result
from lib.load_content import load_content
from lib.search import search


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
