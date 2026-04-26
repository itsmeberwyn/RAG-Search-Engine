import argparse

from lib.common import format_search_result
from lib.index import build_indexes
from lib.search import search


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    subparsers.add_parser("build", help="Build inverted index")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    match args.command:
        case "search":
            results = search(args.query)
            format_search_result(results)
        case "build":
            build_indexes()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
