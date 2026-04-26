from .common import tokens
from .index import InvertedIndex


def search(query: str, limit: int = 5) -> list[dict]:
    results = []
    seen = set()
    index = InvertedIndex()
    index.load()

    query_tokens = tokens(query)
    for query in query_tokens:
        index_results = index.get_documents(query)
        for index_result in index_results:
            if index_result in seen:
                continue
            seen.add(index_result)
            search_result = index.docmap[index_result]
            results.append(search_result)
            if len(results) >= limit:
                return results
    return results
