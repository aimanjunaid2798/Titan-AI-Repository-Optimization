"""
parser.py

Robust parser for Titan Planner responses.
"""

from __future__ import annotations

import json
import re

from titan.planner.models import OptimizationRoadmap


class RoadmapParser:
    """
    Parses LLM output into an OptimizationRoadmap.
    """

    @staticmethod
    def _extract_json(
        response: str,
    ) -> str:
        """
        Extract JSON from raw LLM output.
        """

        response = response.strip()

        # Case 1: Already valid JSON
        if response.startswith("{"):
            return response

        # Case 2: Markdown ```json block
        match = re.search(
            r"```(?:json)?\s*(.*?)```",
            response,
            flags=re.DOTALL,
        )

        if match:
            return match.group(1).strip()

        # Case 3: Find first JSON object
        start = response.find("{")
        end = response.rfind("}")

        if start != -1 and end != -1:
            return response[start:end + 1]

        raise ValueError(
            "No JSON object found in LLM response."
        )

    @classmethod
    def parse(
        cls,
        response: str,
    ) -> OptimizationRoadmap:

        try:

            json_text = cls._extract_json(
                response
            )

            data = json.loads(
                json_text
            )

            return OptimizationRoadmap.model_validate(
                data
            )

        except Exception as error:

            raise ValueError(
                f"Failed to parse planner response.\n\n"
                f"Raw Response:\n{response}"
            ) from error