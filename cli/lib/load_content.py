import json
from pathlib import Path


def load_content() -> list[str]:
    curr_dir = Path(__file__).parent
    movies_path = curr_dir / "../../data/movies.json"
    content = []

    with open(movies_path) as f:
        content = json.load(f)
    return content["movies"]


def load_stopwords() -> list[str]:
    curr_dir = Path(__file__).parent
    movies_path = curr_dir / "../../data/stopwords.txt"
    content = []

    with open(movies_path, "r") as f:
        content = f.read().splitlines()
    return content
