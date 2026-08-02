from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the required model (downloads once, then caches)
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Cache
cached_texts = None
cached_embeddings = None


def semantic_search(query: str, notes: list):
    """
    Semantic search using sentence embeddings.

    notes = [
        {
            "id": ...,
            "title": "...",
            "content": "...",
            ...
        }
    ]
    """

    global cached_texts
    global cached_embeddings

    if not notes:
        return []

    # Combine title and content
    texts = [
        f"{note['title']} {note['content']}"
        for note in notes
    ]

    # Compute note embeddings only if notes changed
    if cached_texts != texts:

        cached_texts = texts

        cached_embeddings = model.encode(texts)

    # Compute query embedding every search
    query_embedding = model.encode([query])

    # Cosine similarity
    similarities = cosine_similarity(
        query_embedding,
        cached_embeddings
    )[0]

    results = []

    for i, note in enumerate(notes):

        item = note.copy()

        item["similarity"] = float(similarities[i])

        results.append(item)

    # Manual descending sort (Selection Sort)
    for i in range(len(results)):

        max_index = i

        for j in range(i + 1, len(results)):

            if (
                results[j]["similarity"]
                > results[max_index]["similarity"]
            ):
                max_index = j

        results[i], results[max_index] = (
            results[max_index],
            results[i]
        )

    return results[:3]