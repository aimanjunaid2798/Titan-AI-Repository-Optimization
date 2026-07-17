"""
base.py

Abstract interface for Titan LLM providers.

Author: Titan Team
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Type

from pydantic import BaseModel


class BaseLLMClient(ABC):
    """
    Base interface implemented by every LLM provider.
    """

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        schema: Type[BaseModel],
    ) -> str:
        """
        Generate a structured JSON response.

        Parameters
        ----------
        system_prompt : str
        user_prompt : str
        schema : Type[BaseModel]
            Expected Pydantic model.

        Returns
        -------
        str
            Raw JSON returned by the model.
        """

        raise NotImplementedError