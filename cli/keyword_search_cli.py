import argparse

from lib.common import format_search_result
from lib.index import build_indexes, get_term_frequencies
from lib.search import search


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available Commands")

    subparsers.add_parser("build", help="Build inverted index")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    doc_id_parser = subparsers.add_parser("tf", help="Check for term frequency for specific ID")
    doc_id_parser.add_argument("doc_id", type=str, help="Document Id")
    doc_id_parser.add_argument("term", type=str, help="Term for specific document")

    args = parser.parse_args()

    match args.command:
        case "search":
            results = search(args.query)
            format_search_result(results)
        case "build":
            build_indexes()
        case "tf":
            get_term_frequencies(int(args.doc_id), args.term)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
