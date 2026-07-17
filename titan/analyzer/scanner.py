"""
scanner.py

Main orchestrator for repository analysis.

The scanner coordinates all analysis modules and builds
a RepositoryProfile object.

Author: Titan Team
"""

from __future__ import annotations

import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from titan.models.repository import RepositoryProfile
from titan.models.analyzer import (
    LanguageDetectionResult,
    FrameworkDetectionResult,
    GPUDetectionResult,
    RepositoryTypeDetectionResult,
)

from titan.analyzer.language_detector import LanguageDetector
from titan.analyzer.framework_detector import FrameworkDetector
from titan.analyzer.gpu_detector import GPUDetector

from titan.opportunity.engine import OpportunityEngine

from titan.analyzer.repository_type_detector import (
    RepositoryTypeDetector,
)

logger = logging.getLogger(__name__)


class RepositoryScanner:
    """
    Orchestrates the complete repository analysis.

    The scanner never performs repository analysis itself.
    Instead, it coordinates specialized detectors and
    assembles a RepositoryProfile consumed by downstream
    agents.
    """

    def __init__(self, repository_path: str):

        self.repository_path = Path(
            repository_path
        ).resolve()

        if not self.repository_path.exists():
            raise FileNotFoundError(
                f"Repository not found: {self.repository_path}"
            )

        if not self.repository_path.is_dir():
            raise NotADirectoryError(
                f"{self.repository_path} is not a directory."
            )

        # Register detectors
        self.detectors = {
            "language": LanguageDetector(
                self.repository_path
            ),
            "framework": FrameworkDetector(
                self.repository_path
            ),
            "gpu": GPUDetector(
                self.repository_path
            ),
            "repository_type": RepositoryTypeDetector(
                self.repository_path
            ),
        }

        # Shared opportunity engine
        self.opportunity_engine = OpportunityEngine()

    def _run_detector(
        self,
        detector: Any,
        fallback: Any,
        detector_name: str,
    ) -> Any:
        """
        Execute a detector safely.

        If detection fails, log the exception and return
        the provided fallback result.
        """

        try:
            return detector.detect()

        except Exception:

            logger.exception(
                "%s failed.",
                detector_name,
            )

            return fallback

    def scan(self) -> RepositoryProfile:
        """
        Execute the complete repository analysis.
        """

        analysis_start = time.perf_counter()

        language_result = self._run_detector(
            self.detectors["language"],
            LanguageDetectionResult(),
            "Language Detector",
        )

        framework_result = self._run_detector(
            self.detectors["framework"],
            FrameworkDetectionResult(),
            "Framework Detector",
        )

        gpu_result = self._run_detector(
            self.detectors["gpu"],
            GPUDetectionResult(),
            "GPU Detector",
        )

        repository_type_result = self._run_detector(
            self.detectors["repository_type"],
            RepositoryTypeDetectionResult(),
            "Repository Type Detector",
        )

        profile = self._build_profile(
            language_result=language_result,
            framework_result=framework_result,
            gpu_result=gpu_result,
            repository_type_result=repository_type_result,
        )

        profile.analysis_duration = round(
            time.perf_counter() - analysis_start,
            3,
        )

        print("Frameworks:", profile.frameworks)
        print("GPU:", profile.gpu_backends)

        profile.opportunities = (
            self.opportunity_engine.analyze(profile)
        )

        return profile

    def _build_profile(
        self,
        language_result,
        framework_result,
        gpu_result,
        repository_type_result,
    ) -> RepositoryProfile:
        """
        Build the RepositoryProfile from detector outputs.
        """

        repository_name = (
            self.repository_path.name
            if self.repository_path.name
            else self.repository_path.resolve().name
        )

        return RepositoryProfile(
            repository_name=repository_name,
            repository_path=str(self.repository_path),

            statistics=language_result.statistics,

            languages=language_result.languages,

            frameworks=framework_result.frameworks,

            gpu_backends=gpu_result.gpu_backends,

            analysis_timestamp=datetime.now(
                timezone.utc
            ),

            metadata={
                "training_detected": False,
                "inference_detected": False,
                "rag_detected": False,
                "cli_detected": False,
                "ai_infrastructure_detected": False,
            }
        )