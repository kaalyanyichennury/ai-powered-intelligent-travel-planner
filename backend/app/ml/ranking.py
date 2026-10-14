from typing import List, Dict, Any

class MultiCriteriaRanker:
    @staticmethod
    def rerank_diverse_attractions(
        attractions: List[Dict[str, Any]],
        max_items_per_category: int = 2
    ) -> List[Dict[str, Any]]:
        """
        Reranks scored attractions to ensure category diversity
        (e.g., prevents having only museums or only churches),
        while maintaining high recommendation relevance.
        """
        category_counts: Dict[str, int] = {}
        primary_picks = []
        secondary_picks = []

        for item in attractions:
            cat = item.get("category", "General")
            count = category_counts.get(cat, 0)
            if count < max_items_per_category:
                category_counts[cat] = count + 1
                primary_picks.append(item)
            else:
                secondary_picks.append(item)

        return primary_picks + secondary_picks

ranking_engine = MultiCriteriaRanker()
