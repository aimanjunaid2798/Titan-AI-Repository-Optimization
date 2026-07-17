"""
parser.py

Verification models.

Author: Titan Team
"""

from __future__ import annotations

import json
import re

from titan.verifier.models import (
    VerificationResult,
)


class VerificationParser:
    """
    Parses verifier responses.
    """

    @staticmethod
    def parse(
        response: str,
    ) -> VerificationResult:

        response = response.strip()

        # Remove markdown fences
        response = re.sub(
            r"^```(?:json)?",
            "",
            response,
            flags=re.IGNORECASE | re.MULTILINE,
        )

        response = re.sub(
            r"```$",
            "",
            response,
            flags=re.MULTILINE,
        ).strip()

        # Extract JSON
        start = response.find("{")
        end = response.rfind("}")

        if start == -1 or end == -1:

            raise ValueError(
                "Verifier returned no JSON."
            )

        response = response[
            start:end + 1
        ]

        try:

            data = json.loads(
                response
            )

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Invalid verifier JSON:\n\n{response}"
            ) from error

        return VerificationResult(
            **data
        )