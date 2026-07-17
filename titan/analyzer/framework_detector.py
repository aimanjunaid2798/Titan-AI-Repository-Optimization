"""
framework_detector.py

Detect frameworks used by a repository.

Author: Titan Team
"""

from __future__ import annotations

from pathlib import Path

from titan.config.config_loader import ConfigLoader
from titan.models.analyzer import FrameworkDetectionResult
from titan.utils.repository_walker import RepositoryWalker


class FrameworkDetector:
    """
    Detects frameworks by scanning Python import
    statements.
    """

    PYTHON_EXTENSIONS = {
        ".py"
    }

    def __init__(
        self,
        repository_path: Path,
    ):

        self.repository_path = repository_path

        self.framework_map = ConfigLoader.load(
            "frameworks.json"
        )

        self.walker = RepositoryWalker(
            repository_path
        )

    def detect(
        self,
    ) -> FrameworkDetectionResult:

        detected_frameworks = set()

        scanned_files = 0

        for path in self.walker.iter_files(
            extensions=self.PYTHON_EXTENSIONS
        ):

            scanned_files += 1

            content = self.walker.read_text_file(
                path
            )

            for (
                framework,
                patterns,
            ) in self.framework_map.items():

                if any(
                    pattern in content
                    for pattern in patterns
                ):
                    detected_frameworks.add(
                        framework
                    )

        return FrameworkDetectionResult(

            frameworks=sorted(
                detected_frameworks
            ),

            scanned_files=scanned_files,
        )