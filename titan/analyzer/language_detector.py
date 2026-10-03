"""
language_detector.py

Detect programming languages and repository statistics.

Author: Titan Team
"""

from __future__ import annotations
from pathlib import Path

from titan.models.repository import RepositoryStatistics
from titan.models.analyzer import LanguageDetectionResult

from titan.config.config_loader import ConfigLoader

from titan.utils.repository_walker import RepositoryWalker


class LanguageDetector:
    """
    Detects programming languages inside a repository.
    """

    IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        "venv",
        ".venv",
        "node_modules",
        "dist",
        "build",
        ".idea",
        ".vscode",
        ".pytest_cache",
        ".mypy_cache",
    }

    def __init__(self, repository_path: Path):

        self.repository_path = repository_path

        self.language_map = ConfigLoader.load(
            "languages.json"
        )

    def detect(self) -> LanguageDetectionResult:

        languages = {}

        detected_extensions = set()

        total_files = 0

        total_lines = 0

        ignored_files = 0

        largest_file = None

        largest_lines = 0

        walker = RepositoryWalker(
            self.repository_path
        )

        for path in walker.iter_files():

            if self._should_ignore(path):

                ignored_files += 1

                continue

            if not path.is_file():

                continue

            total_files += 1

            suffix = path.suffix.lower()

            language = self._find_language(suffix)

            if language is None:

                continue

            detected_extensions.add(suffix)

            line_count = self._count_lines(path)

            total_lines += line_count

            languages[language] = (
                languages.get(language, 0) + 1
            )

            if line_count > largest_lines:

                largest_lines = line_count

                largest_file = str(path)

        statistics = RepositoryStatistics(

            total_files=total_files,

            total_lines=total_lines,

            largest_file=largest_file,
        )

        return LanguageDetectionResult(

            languages=languages,

            statistics=statistics,

            scanned_files=total_files,

            ignored_files=ignored_files,

            detected_extensions=sorted(
                detected_extensions
            ),
        )

    def _find_language(
        self,
        suffix: str,
    ) -> str | None:

        for language, extensions in self.language_map.items():

            if suffix in extensions:

                return language

        return None

    def _should_ignore(
        self,
        path: Path,
    ) -> bool:

        return any(
            part in self.IGNORED_DIRECTORIES
            for part in path.parts
        )

    @staticmethod
    def _count_lines(
        path: Path,
    ) -> int:

        try:

            with open(
                path,
                encoding="utf-8",
                errors="ignore",
            ) as file:

                return sum(
                    1 for _
                    in file
                )

        except Exception:

            return 0