import json
import logging
import os
from typing import Any, Dict, List, Optional

import requests

logger = logging.getLogger(__name__)


class GeminiError(RuntimeError):
    status_code = 502


class GeminiConfigurationError(GeminiError):
    status_code = 503


class GeminiService:
    MODEL = "gemini-2.5-flash"
    API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    TIMEOUT_SECONDS = 30

    @property
    def model(self) -> str:
        return os.getenv("GEMINI_MODEL", self.MODEL).strip() or self.MODEL

    @property
    def is_configured(self) -> bool:
        return bool(os.getenv("GEMINI_API_KEY", "").strip())

    def generate_content(
        self,
        contents: List[Dict[str, Any]],
        system_instruction: Optional[str] = None,
        response_mime_type: Optional[str] = None,
    ) -> str:
        api_key = os.getenv("GEMINI_API_KEY", "").strip()
        if not api_key:
            raise GeminiConfigurationError(
                "Gemini is not configured. Set GEMINI_API_KEY in the backend environment."
            )

        payload: Dict[str, Any] = {"contents": contents}
        if system_instruction:
            payload["systemInstruction"] = {"parts": [{"text": system_instruction}]}
        if response_mime_type:
            payload["generationConfig"] = {"responseMimeType": response_mime_type}

        try:
            response = requests.post(
                self.API_URL.format(model=self.model),
                headers={"x-goog-api-key": api_key},
                json=payload,
                timeout=self.TIMEOUT_SECONDS,
            )
        except requests.RequestException as exc:
            logger.warning("Gemini request failed: %s", exc)
            raise GeminiError("Could not reach the Gemini API.") from exc

        if not response.ok:
            try:
                error_message = response.json().get("error", {}).get("message")
            except (ValueError, AttributeError):
                error_message = None
            detail = f" Gemini API returned HTTP {response.status_code}."
            if error_message:
                detail += f" {error_message}"
            logger.warning("Gemini API request failed with HTTP %s.", response.status_code)
            raise GeminiError(f"Gemini request failed.{detail}")

        try:
            result = response.json()
            parts = result["candidates"][0]["content"]["parts"]
            text = "".join(part["text"] for part in parts if isinstance(part.get("text"), str))
        except (AttributeError, ValueError, KeyError, IndexError, TypeError) as exc:
            raise GeminiError("Gemini returned an empty or invalid response.") from exc

        if not text.strip():
            raise GeminiError("Gemini returned an empty response.")
        return text.strip()

    def generate_json(self, contents: List[Dict[str, Any]], system_instruction: str) -> Dict[str, Any]:
        response_text = self.generate_content(
            contents,
            system_instruction=system_instruction,
            response_mime_type="application/json",
        )
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError as exc:
            raise GeminiError("Gemini returned invalid JSON for a structured request.") from exc
        if not isinstance(result, dict):
            raise GeminiError("Gemini returned JSON in an unexpected format.")
        return result


gemini_service = GeminiService()
