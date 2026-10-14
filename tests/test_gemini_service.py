from types import SimpleNamespace

import pytest
import requests

from backend.app.nlp.parser import NLPParser
from backend.app.rag.retriever import TravelRAGRetriever
from backend.app.rag.vector_store import vector_store
from backend.app.services.gemini_service import (
    GeminiConfigurationError,
    GeminiError,
    gemini_service,
)


def test_gemini_requires_api_key(monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    with pytest.raises(GeminiConfigurationError, match="Set GEMINI_API_KEY"):
        gemini_service.generate_content([{"role": "user", "parts": [{"text": "Hello"}]}])


def test_gemini_uses_configured_model_and_api_key_header(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setenv("GEMINI_MODEL", "gemini-test-model")
    call = {}

    def fake_post(url, **kwargs):
        call.update(url=url, **kwargs)
        return SimpleNamespace(
            ok=True,
            json=lambda: {
                "candidates": [{"content": {"parts": [{"text": "Hello"}, {"text": " there"}]}}]
            },
        )

    monkeypatch.setattr(requests, "post", fake_post)

    result = gemini_service.generate_content(
        [{"role": "user", "parts": [{"text": "Hi"}]}],
        system_instruction="Be helpful.",
    )

    assert result == "Hello there"
    assert call["url"].endswith("/models/gemini-test-model:generateContent")
    assert call["headers"] == {"x-goog-api-key": "test-key"}
    assert call["json"]["systemInstruction"]["parts"][0]["text"] == "Be helpful."
    assert call["timeout"] == gemini_service.TIMEOUT_SECONDS


def test_gemini_provider_errors_are_not_silently_ignored(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        requests,
        "post",
        lambda *args, **kwargs: SimpleNamespace(
            ok=False,
            status_code=429,
            json=lambda: {"error": {"message": "Rate limit exceeded"}},
        ),
    )

    with pytest.raises(GeminiError, match="Rate limit exceeded"):
        gemini_service.generate_content([{"role": "user", "parts": [{"text": "Hello"}]}])


def test_parser_refines_local_extraction_with_gemini(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        gemini_service,
        "generate_json",
        lambda **kwargs: {
            "destination": "Kyoto",
            "duration_days": 5,
            "travelers": 3,
            "budget": 1800,
            "currency": "EUR",
            "interests": ["gardens", "food"],
            "travel_month": "October",
        },
    )

    result = NLPParser().parse_query("Plan a quiet trip to Kyoto")

    assert result.destination == "Kyoto"
    assert result.duration_days == 5
    assert result.interests == ["gardens", "food"]
    assert result.raw_query == "Plan a quiet trip to Kyoto"


def test_rag_uses_gemini_with_retrieved_context_and_chat_history(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(
        vector_store,
        "search",
        lambda *args, **kwargs: [{
            "content": "Use the metro to reach the historic center.",
            "source": "city_guide.txt",
            "title": "Transit",
            "score": 0.8,
        }],
    )
    captured = {}

    def fake_generate(contents, system_instruction=None, response_mime_type=None):
        captured["contents"] = contents
        captured["system_instruction"] = system_instruction
        return "The metro is a convenient option."

    monkeypatch.setattr(gemini_service, "generate_content", fake_generate)

    result = TravelRAGRetriever().answer_question(
        "How do I get there?",
        city_context="Rome",
        conversation_history=[
            {"role": "ai", "content": "Where would you like to go?"},
            {"role": "user", "content": "I am staying in Rome."},
            {"role": "ai", "content": "Rome has an extensive metro."},
            {"role": "user", "content": "How do I get there?"},
        ],
    )

    assert result["answer"] == "The metro is a convenient option."
    assert result["sources"] == ["city_guide.txt (Transit)"]
    assert "Use the metro" in captured["system_instruction"]
    assert captured["contents"] == [
        {"role": "user", "parts": [{"text": "I am staying in Rome."}]},
        {"role": "model", "parts": [{"text": "Rome has an extensive metro."}]},
        {"role": "user", "parts": [{"text": "How do I get there?"}]},
    ]


def test_rag_propagates_gemini_failure_when_configured(monkeypatch):
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    monkeypatch.setattr(vector_store, "search", lambda *args, **kwargs: [])

    def fail_generation(*args, **kwargs):
        raise GeminiError("Gemini API unavailable")

    monkeypatch.setattr(gemini_service, "generate_content", fail_generation)

    with pytest.raises(GeminiError, match="Gemini API unavailable"):
        TravelRAGRetriever().answer_question("What should I visit?")
