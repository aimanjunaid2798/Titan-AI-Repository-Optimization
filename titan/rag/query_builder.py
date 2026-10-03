"""
query_builder.py

Semantic retrieval query builder.

Author: Titan Team
"""

from __future__ import annotations

from titan.knowledge import RepositoryKnowledge


class RetrievalQueryBuilder:
    """
    Generates semantic retrieval queries that
    closely match implementation files.
    """

    def build(
        self,
        knowledge: RepositoryKnowledge,
    ) -> list[str]:

        queries = []

        # -------------------------------------------------
        # Repository
        # -------------------------------------------------

        queries.append(
            f"{knowledge.repository_name} implementation"
        )

        queries.append(
            f"{knowledge.repository_name} architecture"
        )

        # -------------------------------------------------
        # Frameworks
        # -------------------------------------------------

        for framework in knowledge.frameworks:

            queries.extend(
                [
                    f"{framework} implementation",
                    f"{framework} inference",
                    f"{framework} training",
                    f"{framework} optimization",
                ]
            )

        # -------------------------------------------------
        # GPU Backends
        # -------------------------------------------------

        for backend in knowledge.gpu_backends:

            queries.extend(
                [
                    f"{backend} implementation",
                    f"{backend} optimization",
                    f"{backend} performance",
                    f"{backend} inference",
                    f"{backend} training",
                ]
            )

        # -------------------------------------------------
        # Optimization Targets
        # -------------------------------------------------

        for target in knowledge.optimization_targets:

            queries.append(target)

        # -------------------------------------------------
        # Deterministic Opportunities
        # -------------------------------------------------

        for opportunity in knowledge.opportunities:

            title = opportunity.title.lower()

            queries.append(opportunity.title)

            queries.append(opportunity.description)

            queries.append(opportunity.recommendation)

            # -----------------------------
            # GPU Opportunities
            # -----------------------------

            if (
                "mixed precision" in title
                or "amp" in title
            ):

                queries.extend(
                    [
                        "torch.cuda.amp",
                        "torch.amp",
                        "autocast",
                        "GradScaler",
                        "mixed precision",
                        "CUDA AMP",
                        "GPU inference",
                        "GPU training",
                    ]
                )

            if "cuda" in title:

                queries.extend(
                    [
                        "CUDA kernels",
                        "CUDA implementation",
                        "CUDA inference",
                        "GPU implementation",
                    ]
                )

            if "tensorrt" in title:

                queries.extend(
                    [
                        "TensorRT",
                        "TensorRT optimization",
                        "TensorRT inference",
                    ]
                )

            if "onnx" in title:

                queries.extend(
                    [
                        "ONNX",
                        "ONNX Runtime",
                        "model export",
                    ]
                )

        # -------------------------------------------------
        # Engineering Queries
        # -------------------------------------------------

        queries.extend(
            [
                "GPU implementation",
                "model implementation",
                "training implementation",
                "inference implementation",
                "repository optimization",
                "performance optimization",
            ]
        )

        # -------------------------------------------------
        # Remove duplicates
        # -------------------------------------------------

        seen = set()

        unique_queries = []

        for query in queries:

            query = query.strip()

            if (
                query
                and query not in seen
            ):

                seen.add(query)

                unique_queries.append(query)

        return unique_queries