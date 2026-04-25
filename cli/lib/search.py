from .common import tokens


def search(query: str, movies: list[dict], limit: int = 5) -> list[dict]:
    results = []
    for movie in movies:
        title = movie["title"]
        search_query = query

        title_tokens = tokens(title)
        query_tokens = tokens(search_query)

        for query_token in query_tokens:
            for title_token in title_tokens:
                if query_token in title_token and len(results) < limit:
                    results.append(movie)
    return results
