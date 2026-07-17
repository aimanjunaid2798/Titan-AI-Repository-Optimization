"""
repository.py

Core data models shared across every Titan agent.

Author: Titan Team
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from datetime import datetime

from pydantic import BaseModel, Field


class RepositoryStatistics(BaseModel):
    """
    Basic repository statistics.
    """

    total_files: int = 0
    total_directories: int = 0
    total_lines: int = 0
    largest_file: Optional[str] = None


class BuildInformation(BaseModel):
    """
    Information about how the repository is built.
    """

    build_system: Optional[str] = None
    package_manager: Optional[str] = None
    docker_enabled: bool = False
    ci_enabled: bool = False


class RepositoryHealth(BaseModel):
    """
    Repository maturity metrics.
    """

    architecture: int = Field(default=0, ge=0, le=100)
    documentation: int = Field(default=0, ge=0, le=100)
    testing: int = Field(default=0, ge=0, le=100)
    observability: int = Field(default=0, ge=0, le=100)
    security: int = Field(default=0, ge=0, le=100)

    overall_score: int = Field(default=0, ge=0, le=100)


class OptimizationOpportunity(BaseModel):
    """
    Represents an optimization opportunity discovered
    during repository analysis.
    """

    title: str

    category: str

    description: str

    reason: str

    recommendation: str

    expected_impact: str

    confidence: float = Field(
        ge=0,
        le=100,
    )

    detector: str

    priority: str = "Medium"


class RepositoryProfile(BaseModel):
    """
    Master object shared across the Titan pipeline.

    Every agent receives and updates this object.
    """

    repository_name: str
    repository_path: str

    statistics: RepositoryStatistics

    languages: Dict[str, int] = Field(default_factory=dict)

    frameworks: List[str] = Field(default_factory=list)

    gpu_backends: List[str] = Field(default_factory=list)

    build: BuildInformation = Field(
        default_factory=BuildInformation
    )

    health: RepositoryHealth = Field(
        default_factory=RepositoryHealth
    )

    dependencies: List[str] = Field(default_factory=list)

    test_framework: Optional[str] = None

    entry_points: List[str] = Field(default_factory=list)
    architecture_summary: Optional[str] = None

    analysis_timestamp: Optional[datetime] = None

    analysis_duration: Optional[float] = None

    opportunities: List[OptimizationOpportunity] = Field(default_factory=list)

    metadata: Dict[str, Any] = Field(default_factory=dict)