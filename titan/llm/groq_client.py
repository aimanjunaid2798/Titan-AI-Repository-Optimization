"""Groq API implementation for Titan."""

from __future__ import annotations

import os
from typing import Type

import requests
from pydantic import BaseModel

from titan.llm.base import BaseLLMClient


class GroqClient(BaseLLMClient):
    """Hosted Groq client implementing Titan's provider-neutral LLM interface."""

    API_URL = "https://api.groq.com/openai/v1/chat/completions"

    def __init__(
        self,
        model: str | None = None,
        api_key: str | None = None,
        timeout: int = 300,
    ):
        self.model = model or os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.timeout = timeout

        if not self.api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured. Add it to the environment "
                "or Streamlit secrets before running Titan."
            )

    def _request(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel] | None = None,
    ) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": (
                    f"{user_prompt}\n\n"
                    "Return only the requested JSON object. Do not add commentary."
                ),
            },
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0,
            "stream": False,
        }

        if schema is not None:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": schema.__name__.lower(),
                    "strict": False,
                    "schema": schema.model_json_schema(),
                },
            }
        else:
            payload["response_format"] = {"type": "json_object"}

        response = requests.post(
            self.API_URL,
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )

        # Some schemas may contain constructs outside Groq's supported JSON
        # Schema subset. Fall back to JSON mode rather than breaking Titan.
        if response.status_code >= 400 and schema is not None:
            fallback = {
                "model": self.model,
                "messages": messages,
                "temperature": 0,
                "stream": False,
                "response_format": {"type": "json_object"},
            }
            response = requests.post(
                self.API_URL,
                headers=headers,
                json=fallback,
                timeout=self.timeout,
            )

        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"].strip()

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel] | None = None,
    ) -> str:
        return self._request(system_prompt, user_prompt, schema)
