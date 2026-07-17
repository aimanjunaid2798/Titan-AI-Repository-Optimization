"""
engine.py

Central opportunity engine.

Converts repository facts into structured
optimization opportunities.

Author: Titan Team
"""

from __future__ import annotations

from titan.models.repository import (
    RepositoryProfile,
    OptimizationOpportunity,
)

from titan.opportunity.gpu_rules import (
    GPURules,
)

from titan.opportunity.framework_rules import (
    FrameworkRules,
)


class OpportunityEngine:
    """
    Converts analyzer outputs into optimization
    opportunities.
    """

    def analyze(
        self,
        profile: RepositoryProfile,
    ) -> list[OptimizationOpportunity]:

        opportunities = []

        opportunities.extend(

            GPURules.generate(profile)

        )

        opportunities.extend(

            FrameworkRules.generate(profile)

        )

        return opportunities