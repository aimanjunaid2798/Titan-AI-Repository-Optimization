"""
models.py

Repository classification models.

Author: Titan Team
"""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class RepositoryType(str, Enum):

    TRAINING = "Training"

    INFERENCE = "Inference"

    RAG = "RAG"

    AI_INFRASTRUCTURE = "AI Infrastructure"

    BACKEND = "Backend API"

    LIBRARY = "Library"

    CLI = "CLI"

    UNKNOWN = "Unknown"


class RepositoryClassification(BaseModel):

    repository_types: list[RepositoryType]

    confidence: int

    reasoning: list[str]