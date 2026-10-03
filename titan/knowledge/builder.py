"""
builder.py

Builds RepositoryKnowledge from RepositoryProfile.

Author: Titan Team
"""

from __future__ import annotations

from titan.knowledge.models import RepositoryKnowledge
from titan.models.repository import RepositoryProfile


class KnowledgeBuilder:
    """
    Converts RepositoryProfile into structured
    RepositoryKnowledge.
    """

    def build(
        self,
        profile: RepositoryProfile,
    ) -> RepositoryKnowledge:

        technologies = sorted(
            set(
                list(profile.languages.keys())
                + profile.frameworks
                + profile.gpu_backends
            )
        )

        optimization_targets = []

        if profile.gpu_backends:
            optimization_targets.append(
                "GPU Performance"
            )

        if "PyTorch" in profile.frameworks:
            optimization_targets.append(
                "Model Inference"
            )

        return RepositoryKnowledge(

            repository_name=profile.repository_name,

            repository_path=profile.repository_path,

            statistics=profile.statistics,

            languages=sorted(
                profile.languages.keys()
            ),

            frameworks=profile.frameworks,

            gpu_backends=profile.gpu_backends,

            technologies=technologies,

            optimization_targets=optimization_targets,

            risks=[],

            opportunities=profile.opportunities,
        )