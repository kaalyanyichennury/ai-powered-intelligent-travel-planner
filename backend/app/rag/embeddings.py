import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class TextEmbeddingEngine:
    """Embeds text chunks and queries for vector similarity retrieval."""
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=2500,
            sublinear_tf=True
        )
        self.is_fitted = False

    def fit(self, texts: list[str]):
        if texts:
            self.vectorizer.fit(texts)
            self.is_fitted = True

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        if not self.is_fitted:
            self.fit(texts)
        return self.vectorizer.transform(texts).toarray()

    def embed_query(self, query: str) -> np.ndarray:
        if not self.is_fitted:
            return np.zeros((1, 10))
        return self.vectorizer.transform([query]).toarray()

embedding_engine = TextEmbeddingEngine()
