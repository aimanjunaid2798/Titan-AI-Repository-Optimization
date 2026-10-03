"""
config_loader.py

Centralized configuration loader for Titan.

All detectors should load their configuration
through this class instead of reading JSON files
directly.

Author: Titan Team
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class ConfigLoader:
    """
    Loads JSON configuration files used by Titan.
    """

    CONFIG_DIRECTORY = Path(__file__).parent

    @classmethod
    def load(cls, filename: str) -> dict[str, Any]:
        """
        Load a JSON configuration file.

        Example:
            ConfigLoader.load("languages.json")
        """

        config_path = cls.CONFIG_DIRECTORY / filename

        if not config_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}"
            )

        with config_path.open(
            encoding="utf-8"
        ) as file:

            return json.load(file)