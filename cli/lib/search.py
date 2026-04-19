import string

from .common import remove_stopwords, stem_keywords, tokenize_text


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
                if movie_id not in seen and len(results) < limit and stem_keywords(query_token) in stem_keywords(title_token):
                    seen.add(movie_id)
                    results.append(movie)
    sorted_items = sorted(results, key=lambda x: x["id"])
    return sorted_items
