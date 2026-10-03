"""
ollama_client.py

Ollama implementation for Titan.

Author: Titan Team
"""

from __future__ import annotations

from typing import Type

import requests
from pydantic import BaseModel

from titan.llm.base import BaseLLMClient


class OllamaClient(BaseLLMClient):
    """
    Local Ollama client.
    """

    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        host: str = "http://localhost:11434",
    ):

        self.model = model
        self.host = host.rstrip("/")

    def _request(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel] | None = None,
    ) -> str:

        payload = {

            "model": self.model,

            "system": system_prompt,

            "prompt": user_prompt,

            "stream": False,

            "options": {

                "temperature": 0,

                "top_p": 0.1,

                "num_predict": 2048,

            },
        }

        # Structured Outputs
        if schema is not None:

            payload["format"] = schema.model_json_schema()

        response = requests.post(

            f"{self.host}/api/generate",

            json=payload,

            timeout=300,

        )

        response.raise_for_status()

        return response.json()["response"].strip()

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel] | None = None,
    ) -> str:
        """
        Generate a response.
        """

        response = self._request(

            system_prompt,

            user_prompt,

            schema,

        )

        return response