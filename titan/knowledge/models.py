"""
models.py

Knowledge models shared by Titan agents.

Author: Titan Team
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field

from titan.models.repository import (
    OptimizationOpportunity,
    RepositoryStatistics,
)


class RepositoryKnowledge(BaseModel):
    """
    Structured engineering knowledge derived from
    RepositoryProfile.

    This object contains structured data only.
    Prompt generation is handled separately.
    """

    repository_name: str

    repository_path: str

    statistics: RepositoryStatistics

    languages: List[str] = Field(default_factory=list)

    frameworks: List[str] = Field(default_factory=list)

    gpu_backends: List[str] = Field(default_factory=list)

    technologies: List[str] = Field(default_factory=list)

    optimization_targets: List[str] = Field(default_factory=list)

    risks: List[str] = Field(default_factory=list)

    opportunities: List[
        OptimizationOpportunity
    ] = Field(default_factory=list)