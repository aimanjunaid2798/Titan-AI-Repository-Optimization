"""
repository_walker.py

Shared repository traversal utilities used by all Titan analyzers.

This class is responsible for walking repositories safely,
ignoring unnecessary directories, reading files, and exposing
a clean interface for analyzer modules.

Author: Titan Team
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator


class RepositoryWalker:
    """
    Walks a repository while ignoring directories that
    should never be analyzed.
    """

    DEFAULT_IGNORED_DIRECTORIES = {
        ".git",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".idea",
        ".vscode",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "build",
        "dist",
        "target",
        ".tox",
        ".cache",
    }

    def __init__(
        self,
        repository_path: Path,
        ignored_directories: set[str] | None = None,
    ):

        self.repository_path = repository_path

        self.ignored_directories = (
            ignored_directories
            or self.DEFAULT_IGNORED_DIRECTORIES
        )

    def iter_files(
        self,
        extensions: set[str] | None = None,
    ) -> Iterator[Path]:
        """
        Yield repository files while ignoring excluded
        directories.

        Parameters
        ----------
        extensions:
            Optional set of file extensions to include.
            Example:
                {".py", ".cpp"}
        """

        for path in self.repository_path.rglob("*"):

            if not path.is_file():
                continue

            if self.should_ignore(path):
                continue

            if (
                extensions is not None
                and path.suffix.lower() not in extensions
            ):
                continue

            yield path

    def should_ignore(
        self,
        path: Path,
    ) -> bool:
        """
        Determine whether a path should be ignored.
        """

        return any(
            part in self.ignored_directories
            for part in path.parts
        )

    @staticmethod
    def read_text_file(
        path: Path,
    ) -> str:
        """
        Safely read a text file.
        """

        try:

            return path.read_text(
                encoding="utf-8",
                errors="ignore",
            )

        except Exception:

            return ""

    @staticmethod
    def count_lines(
        path: Path,
    ) -> int:
        """
        Count the number of lines in a file.
        """

        try:

            with path.open(
                encoding="utf-8",
                errors="ignore",
            ) as file:

                return sum(1 for _ in file)

        except Exception:

            return 0

    @staticmethod
    def extension(
        path: Path,
    ) -> str:
        """
        Return a lowercase file extension.
        """

        return path.suffix.lower()