"""
classifier.py

Repository classifier.

Author: Titan Team
"""

from __future__ import annotations

from titan.classifier.models import (
    RepositoryClassification,
)

from titan.classifier.rules import (
    ClassificationRules,
)

from titan.models.repository import (
    RepositoryProfile,
)


class RepositoryClassifier:
    """
    Deterministic repository classifier.
    """

    def classify(
        self,
        profile: RepositoryProfile,
    ) -> RepositoryClassification:

        repository_types, reasoning = (
            ClassificationRules.classify(
                profile
            )
        )

        confidence = min(
            100,
            60 + len(reasoning) * 10,
        )

        return RepositoryClassification(
            repository_types=repository_types,
            confidence=confidence,
            reasoning=reasoning,
        )