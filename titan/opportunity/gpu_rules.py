"""
gpu_rules.py

GPU optimization rules.

Author: Titan Team
"""

from __future__ import annotations

from titan.models.repository import (
    RepositoryProfile,
    OptimizationOpportunity,
)


class GPURules:
    """
    Deterministic GPU optimization rules.
    """

    @staticmethod
    def generate(
        profile: RepositoryProfile,
    ) -> list[OptimizationOpportunity]:

        opportunities = []

        gpu_features = profile.metadata.get(
            "gpu_features",
            [],
        )

        training_detected = profile.metadata.get(
            "training_detected",
            False,
        )

        inference_detected = profile.metadata.get(
            "inference_detected",
            False,
        )
        
        if (
            "CUDA" in profile.gpu_backends
            and (
                training_detected
                or inference_detected
            )
            and "Mixed Precision" not in gpu_features
        ):

            opportunities.append(
                OptimizationOpportunity(
                    title="Enable Mixed Precision",
                    category="GPU",
                    description=(
                        "CUDA detected but Automatic "
                        "Mixed Precision was not found."
                    ),
                    reason=(
                        "Mixed precision can significantly "
                        "reduce GPU compute time."
                    ),
                    recommendation=(
                        "Use torch.cuda.amp.autocast "
                        "or torch.amp.autocast."
                    ),
                    expected_impact="15–30%",
                    confidence=94,
                    detector="GPURules",
                    priority="High",
                )
            )

        return opportunities