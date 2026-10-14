import re
from typing import Dict, Any, List, Optional

KNOWN_DESTINATIONS = [
    "Paris", "France", "Tokyo", "Japan", "Rome", "Italy", "New York", "NYC", "United States", "USA",
    "Dubai", "United Arab Emirates", "UAE", "Barcelona", "Spain", "Kyoto", "Bali", "Indonesia",
    "London", "United Kingdom", "UK", "Amsterdam", "Netherlands", "Singapore", "Bangkok", "Thailand",
    "Cape Town", "South Africa", "Rio de Janeiro", "Brazil", "Istanbul", "Turkey", "Cairo", "Egypt",
    "Sydney", "Australia", "Venice", "Florence", "Berlin", "Germany", "Vienna", "Austria",
    "Prague", "Czech Republic", "Madrid", "Seoul", "South Korea", "Zurich", "Switzerland"
]

INTEREST_KEYWORDS = {
    "history": ["history", "historical", "ancient", "monument", "heritage", "ruins", "castle", "palace", "archaeology"],
    "food": ["food", "dining", "culinary", "cuisine", "restaurants", "street food", "ramen", "pasta", "gastronomy", "wine", "eating"],
    "photography": ["photography", "photos", "picturesque", "scenic", "viewpoints", "instagram", "photo"],
    "art": ["art", "museums", "galleries", "paintings", "sculpture", "exhibitions", "louvre"],
    "architecture": ["architecture", "buildings", "cathedral", "church", "towers", "skyscrapers", "gothic", "baroque"],
    "temples": ["temples", "temple", "shrine", "shrines", "pagoda", "spiritual", "mosque", "buddhism"],
    "anime": ["anime", "manga", "gaming", "cosplay", "otaku", "akihabara", "pop culture"],
    "nature": ["nature", "parks", "gardens", "greenery", "mountains", "lakes", "outdoor", "forest"],
    "adventure": ["adventure", "hiking", "cable car", "safari", "dune bashing", "thrill", "climbing"],
    "shopping": ["shopping", "malls", "bazaars", "boutiques", "markets", "fashion", "souvenirs"],
    "nightlife": ["nightlife", "bars", "clubs", "pubs", "evening", "cocktails", "entertainment"],
    "relaxation": ["relaxation", "peaceful", "quiet", "wellness", "spa", "chill", "leisure"]
}

MONTHS = [
    "january", "february", "march", "april", "may", "june",
    "july", "august", "september", "october", "november", "december"
]

class EntityExtractor:
    @classmethod
    def extract_destination(cls, text: str) -> Optional[str]:
        # Direct regex patterns: "trip to X", "visit X", "going to X", "travel to X", "in X for"
        match = re.search(r"(?:trip to|visit|travel to|going to|vacation in|holiday in|tour of)\s+([A-Za-z\s]+?)(?:\s+for|\s+with|\s+in|\s+during|\.|$|,)", text, re.IGNORECASE)
        if match:
            cand = match.group(1).strip()
            # Clean up common stop words
            cand = re.sub(r"^(a|an|the)\s+", "", cand, flags=re.IGNORECASE)
            if cand and len(cand) > 2:
                return cand.title()

        # Check known list
        for dest in KNOWN_DESTINATIONS:
            if re.search(r"\b" + re.escape(dest) + r"\b", text, re.IGNORECASE):
                return dest

        return None

    @classmethod
    def extract_duration(cls, text: str) -> int:
        # e.g., "7-day", "7 days", "10 days", "for 5 days", "2 weeks", "weekend"
        match = re.search(r"(\d+)\s*(?:-| )?days?", text, re.IGNORECASE)
        if match:
            return max(1, min(30, int(match.group(1))))

        match_weeks = re.search(r"(\d+)\s*(?:-| )?weeks?", text, re.IGNORECASE)
        if match_weeks:
            return max(1, min(30, int(match_weeks.group(1)) * 7))

        if re.search(r"\bweekend\b", text, re.IGNORECASE):
            return 3

        return 7  # Standard default

    @classmethod
    def extract_travelers(cls, text: str) -> int:
        match = re.search(r"(?:for|with)\s+(\d+)\s*(?:people|persons|travelers|travellers|adults|guests)", text, re.IGNORECASE)
        if match:
            return max(1, min(20, int(match.group(1))))

        if re.search(r"\b(?:solo|alone|myself)\b", text, re.IGNORECASE):
            return 1
        if re.search(r"\b(?:couple|two of us|two people|for 2)\b", text, re.IGNORECASE):
            return 2
        if re.search(r"\bfamily of (\d+)\b", text, re.IGNORECASE):
            return int(re.search(r"\bfamily of (\d+)\b", text, re.IGNORECASE).group(1))

        # Check single digit after for: "for 2"
        match_short = re.search(r"\bfor\s+(\d+)\b", text, re.IGNORECASE)
        if match_short:
            val = int(match_short.group(1))
            if 1 <= val <= 20:
                return val

        return 2

    @classmethod
    def extract_budget_and_currency(cls, text: str) -> tuple[float, str]:
        # Indian Lakh format: "₹1.5 lakh", "1.5 lakh", "2 lakh", "2.5 lakhs"
        match_lakh = re.search(r"(?:₹|rs\.?|inr)?\s*(\d+(?:\.\d+)?)\s*(?:lakh|lakhs|lac|lacs)\b", text, re.IGNORECASE)
        if match_lakh:
            lakh_val = float(match_lakh.group(1))
            return round(lakh_val * 100000.0, 2), "INR"

        # Indian Rupee numeric: "₹ 150000", "₹1,50,000", "150000 inr", "rs 50000"
        match_inr = re.search(r"(?:₹|rs\.?|inr)\s*([\d,]+(?:\.\d+)?)", text, re.IGNORECASE)
        if match_inr:
            num = float(match_inr.group(1).replace(",", ""))
            return num, "INR"
        
        match_inr_post = re.search(r"([\d,]+(?:\.\d+)?)\s*(?:rs|rupees|inr)\b", text, re.IGNORECASE)
        if match_inr_post:
            num = float(match_inr_post.group(1).replace(",", ""))
            return num, "INR"

        # US Dollars: "$2,500", "$ 2500", "2500 usd", "2500 dollars"
        match_usd = re.search(r"\$\s*([\d,]+(?:\.\d+)?)", text)
        if match_usd:
            num = float(match_usd.group(1).replace(",", ""))
            return num, "USD"

        match_usd_post = re.search(r"([\d,]+(?:\.\d+)?)\s*(?:usd|dollars?)\b", text, re.IGNORECASE)
        if match_usd_post:
            num = float(match_usd_post.group(1).replace(",", ""))
            return num, "USD"

        # Euros: "€2,500", "2500 euros", "2500 eur"
        match_eur = re.search(r"€\s*([\d,]+(?:\.\d+)?)", text)
        if match_eur:
            num = float(match_eur.group(1).replace(",", ""))
            return num, "EUR"

        # British Pounds: "£2,000", "2000 gbp"
        match_gbp = re.search(r"£\s*([\d,]+(?:\.\d+)?)", text)
        if match_gbp:
            num = float(match_gbp.group(1).replace(",", ""))
            return num, "GBP"

        # Japanese Yen: "¥150000", "150,000 yen"
        match_jpy = re.search(r"[¥]\s*([\d,]+)", text)
        if match_jpy:
            num = float(match_jpy.group(1).replace(",", ""))
            return num, "JPY"

        # Generic "budget of 2500"
        match_gen = re.search(r"(?:budget\s+of|budget:?)\s*([\d,]+)", text, re.IGNORECASE)
        if match_gen:
            num = float(match_gen.group(1).replace(",", ""))
            return num, "USD"

        return 2500.0, "USD"

    @classmethod
    def extract_interests(cls, text: str) -> List[str]:
        found = set()
        lower = text.lower()
        for interest, kw_list in INTEREST_KEYWORDS.items():
            for kw in kw_list:
                if re.search(r"\b" + re.escape(kw) + r"\b", lower):
                    found.add(interest.title())
                    break
        if not found:
            return ["History", "Food", "Photography"]
        return list(found)

    @classmethod
    def extract_month(cls, text: str) -> Optional[str]:
        lower = text.lower()
        for m in MONTHS:
            if re.search(r"\b" + m + r"\b", lower):
                return m.title()
        return "May"

entity_extractor = EntityExtractor()
