import logging
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class ContentBasedRecommender:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            token_pattern=r"(?u)\b\w+\b"
        )

    def _build_place_corpus(self, places: List[Dict[str, Any]]) -> List[str]:
        corpus = []
        for p in places:
            # Emphasize category and tags by repeating them in the document representation
            doc = (
                f"{p.get('name', '')} {p.get('category', '')} {p.get('category', '')} "
                f"{p.get('description', '')} {p.get('tags', '')} {p.get('tags', '')} "
                f"{p.get('city', '')} {p.get('best_season', '')} {p.get('indoor_outdoor', '')}"
            )
            corpus.append(doc.lower())
        return corpus

    def _build_user_query(self, interests: List[str], pace: str = "balanced") -> str:
        # Repeat interests to give them prominence
        text = " ".join([f"{item} {item}" for item in interests])
        if pace == "intensive":
            text += " adventure skyline walk explore"
        elif pace == "relaxed":
            text += " peaceful garden cafe park leisure"
        return text.lower()

    def recommend(
        self,
        places: List[Dict[str, Any]],
        user_interests: List[str],
        top_k: int = 15,
        weather_rainy: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Calculates compatibility score between user preferences and attractions
        using TF-IDF Vectorization and Cosine Similarity.
        """
        if not places:
            return []

        corpus = self._build_place_corpus(places)
        user_doc = self._build_user_query(user_interests)

        # Vectorize
        try:
            tfidf_matrix = self.vectorizer.fit_transform(corpus + [user_doc])
            place_vectors = tfidf_matrix[:-1]
            user_vector = tfidf_matrix[-1:]

            # Compute Cosine Similarities
            similarities = cosine_similarity(user_vector, place_vectors)[0]
        except Exception as e:
            logger.warning(f"TF-IDF recommendation calculation error: {e}. Using heuristic scoring.")
            similarities = np.array([0.75 for _ in places])

        scored_places = []
        for idx, p in enumerate(places):
            base_sim = float(similarities[idx])
            rating = float(p.get("rating", 4.5))
            
            # Keyword match boost
            tags = p.get("tags", "").lower()
            category = p.get("category", "").lower()
            desc = p.get("description", "").lower()
            kw_matches = sum(1 for interest in user_interests if interest.lower() in tags or interest.lower() in category or interest.lower() in desc)
            kw_boost = min(0.35, kw_matches * 0.12)
            rating_norm = (rating - 3.0) / 2.0  # e.g., 4.8 -> 0.90

            composite_score = (0.50 * base_sim) + (0.20 * rating_norm) + kw_boost

            # Weather penalty/boost
            is_indoor = str(p.get("indoor_outdoor", "")).lower() == "indoor"
            if weather_rainy:
                if is_indoor:
                    composite_score += 0.10
                else:
                    composite_score -= 0.15

            # Scaled percentage
            percentage = min(99, max(65, int(round(60 + (composite_score * 38)))))

            # Determine key match reasons
            reasons = []
            tags = p.get("tags", "").lower()
            category = p.get("category", "").lower()
            for interest in user_interests:
                if interest.lower() in tags or interest.lower() in category or interest.lower() in p.get("description", "").lower():
                    reasons.append(f"Matches your interest in {interest.title()}")

            if rating >= 4.7:
                reasons.append(f"Highly acclaimed destination ({rating}★)")
            if not reasons:
                reasons.append("Top curated cultural landmark")

            p_copy = dict(p)
            p_copy["compatibility_score"] = percentage / 100.0
            p_copy["compatibility_percentage"] = percentage
            p_copy["match_reasons"] = reasons
            scored_places.append(p_copy)

        # Sort descending by compatibility score
        scored_places.sort(key=lambda x: x["compatibility_score"], reverse=True)
        return scored_places[:top_k]

recommender = ContentBasedRecommender()
