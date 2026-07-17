"""
models.py

Planner output models.

Author: Titan Team
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class RoadmapItem(BaseModel):
    """
    A single optimization recommendation.
    """

    priority: int

    title: str

    description: str

    rationale: str

    expected_impact: str

    estimated_speedup: str = "Unknown"

    implementation_difficulty: str = "Medium"

    affected_files: List[str] = Field(
        default_factory=list
    )

    # NEW
    supporting_evidence: List[str] = Field(
        default_factory=list
    )

    implementation_steps: List[str] = Field(
        default_factory=list
    )

    confidence: float = Field(
        ge=0,
        le=100,
    )


class OptimizationRoadmap(BaseModel):
    """
    Complete optimization roadmap generated
    by Titan Planner.
    """

    repository_name: str

    summary: str

    recommendations: List[
        RoadmapItem
    ] = Field(default_factory=list)

    overall_confidence: float = Field(
        ge=0,
        le=100,
    )

    verification_score: int | None = None