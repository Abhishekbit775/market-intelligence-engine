"""
Layer 2 (NLP) — Near-duplicate news removal.

Production design uses sentence-embeddings + FAISS for semantic dedup.
Offline fallback uses a token Jaccard similarity, which removes obvious
re-prints of the same story without needing model downloads.
"""


def _jaccard(a, b):
    sa, sb = set(a.lower().split()), set(b.lower().split())
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def deduplicate(articles, threshold=0.6):
    """articles: list of dicts each with a 'headline' key. Returns unique list."""
    unique = []
    for art in articles:
        if any(_jaccard(art["headline"], u["headline"]) >= threshold for u in unique):
            continue
        unique.append(art)
    return unique
