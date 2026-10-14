import os
import glob
import logging
from typing import List, Dict, Any
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .embeddings import embedding_engine

logger = logging.getLogger(__name__)

class VectorDocument:
    def __init__(self, doc_id: str, content: str, source: str, city: str, title: str):
        self.doc_id = doc_id
        self.content = content
        self.source = source
        self.city = city
        self.title = title

class TravelVectorStore:
    def __init__(self):
        self.docs: List[VectorDocument] = []
        self.vectors: np.ndarray = np.array([])
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.kb_dir = os.path.join(self.base_dir, "data", "knowledge_base")
        self.build_index()

    def build_index(self):
        """Loads and indexes knowledge base text files into vector store."""
        if not os.path.exists(self.kb_dir):
            logger.warning(f"Knowledge base directory {self.kb_dir} not found.")
            return

        raw_chunks = []
        files = glob.glob(os.path.join(self.kb_dir, "*.txt"))
        
        for file_path in files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    text = f.read()

                source_name = os.path.basename(file_path)
                lines = text.split("\n")
                title = "Travel Guide"
                city = "General"
                
                # Extract header metadata if present
                for line in lines[:5]:
                    if line.lower().startswith("title:"):
                        title = line.split(":", 1)[1].strip()
                    elif line.lower().startswith("city:"):
                        city = line.split(":", 1)[1].strip()

                # Chunk by section / double-newline
                sections = text.split("\n\n")
                for idx, section in enumerate(sections):
                    clean = section.strip()
                    if len(clean) > 40:  # Skip tiny fragments
                        doc = VectorDocument(
                            doc_id=f"{source_name}_{idx}",
                            content=clean,
                            source=source_name,
                            city=city,
                            title=title
                        )
                        raw_chunks.append(doc)
            except Exception as e:
                logger.error(f"Failed reading KB file {file_path}: {e}")

        self.docs = raw_chunks
        if self.docs:
            texts = [d.content for d in self.docs]
            embedding_engine.fit(texts)
            self.vectors = embedding_engine.embed_documents(texts)
            logger.info(f"Indexed {len(self.docs)} vector knowledge chunks across {len(files)} files.")

    def search(self, query: str, top_k: int = 3, city_filter: str = None) -> List[Dict[str, Any]]:
        """Searches vector index for top relevant snippets."""
        if not self.docs or self.vectors.size == 0:
            return []

        query_vec = embedding_engine.embed_query(query)
        sims = cosine_similarity(query_vec, self.vectors)[0]

        scored_indices = []
        for idx, sim in enumerate(sims):
            doc = self.docs[idx]
            score = float(sim)
            # Boost if matching destination city
            if city_filter and city_filter.lower() in doc.city.lower():
                score += 0.15
            scored_indices.append((score, idx))

        scored_indices.sort(key=lambda x: x[0], reverse=True)

        results = []
        for score, idx in scored_indices[:top_k]:
            doc = self.docs[idx]
            results.append({
                "content": doc.content,
                "source": doc.source,
                "city": doc.city,
                "title": doc.title,
                "score": round(score, 3)
            })
        return results

vector_store = TravelVectorStore()
