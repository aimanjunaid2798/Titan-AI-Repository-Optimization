"""
analyzer.py

Typed models returned by analyzer modules.
"""

from __future__ import annotations

from typing import Dict, List

from pydantic import BaseModel, Field

from titan.models.repository import (
    OptimizationOpportunity,
    RepositoryStatistics,
)


class LanguageDetectionResult(BaseModel):
    """
    Output of the LanguageDetector.
    """

    languages: Dict[str, int] = Field(default_factory=dict)

    statistics: RepositoryStatistics = Field(
        default_factory=RepositoryStatistics
    )

    scanned_files: int = 0

    ignored_files: int = 0

    detected_extensions: List[str] = Field(
        default_factory=list
    )


class FrameworkDetectionResult(BaseModel):
    """
    Output of the FrameworkDetector.
    """

    frameworks: List[str] = Field(
        default_factory=list
    )

    scanned_files: int = 0


class GPUDetectionResult(BaseModel):

    gpu_backends: List[str] = Field(default_factory=list)

    optimization_features: List[str] = Field(default_factory=list)

    training_detected: bool = False

    inference_detected: bool = False

    rag_detected: bool = False

    scanned_files: int = 0


class RepositoryTypeDetectionResult(BaseModel):
    """
    Repository type detection.
    """

    training_detected: bool = False

    inference_detected: bool = False

    rag_detected: bool = False

    cli_detected: bool =False

    ai_infrastructure_detected: bool = False