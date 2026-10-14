import pytest
from backend.app.rag.vector_store import vector_store
from backend.app.rag.retriever import rag_retriever

def test_vector_store_indexed():
    assert len(vector_store.docs) > 0

def test_rag_retrieval():
    results = vector_store.search("tipping etiquette in Paris", top_k=2)
    assert len(results) > 0

def test_rag_retriever_answer():
    res = rag_retriever.answer_question("What are some historical places in Rome?", "Rome")
    assert "answer" in res
    assert len(res["sources"]) > 0
