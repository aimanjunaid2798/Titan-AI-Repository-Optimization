"""
framework_rules.py

Framework-specific optimization rules.

Author: Titan Team
"""

from __future__ import annotations

from titan.models.repository import (
    RepositoryProfile,
    OptimizationOpportunity,
)


class FrameworkRules:

    @staticmethod
    def generate(
        profile: RepositoryProfile,
    ) -> list[OptimizationOpportunity]:

        opportunities = []

        frameworks = {
            framework.lower()
            for framework in profile.frameworks
        }

        metadata = profile.metadata

        training = metadata.get(
            "training_detected",
            False,
        )

        inference = metadata.get(
            "inference_detected",
            False,
        )

        rag = metadata.get(
            "rag_detected",
            False,
        )

        gpu_features = {
            feature.lower()
            for feature in metadata.get(
                "gpu_features",
                []
            )
        }

        # --------------------------------------------------
        # RAG (Highest Priority)
        # --------------------------------------------------

        rag_stack = {
            "langchain",
            "langgraph",
            "chromadb",
            "faiss",
            "qdrant",
            "sentence-transformers",
        }

        if rag or rag_stack.intersection(frameworks):

            opportunities.append(
                OptimizationOpportunity(
                    title="Optimize Retrieval Pipeline",
                    category="RAG",
                    description=(
                        "Retrieval pipeline detected."
                    ),
                    reason=(
                        "Retrieval latency and embedding performance "
                        "are primary bottlenecks in RAG systems."
                    ),
                    recommendation=(
                        "Evaluate embedding caching, incremental indexing, "
                        "retrieval benchmarking and query optimization."
                    ),
                    expected_impact="15-40%",
                    confidence=95,
                    detector="FrameworkRules",
                    priority="High",
                )
            )

        # --------------------------------------------------
        # PyTorch Training
        # --------------------------------------------------

        if (
            "pytorch" in frameworks
            and training
        ):

            if "mixed_precision" not in gpu_features:

                opportunities.append(
                    OptimizationOpportunity(
                        title="Enable Mixed Precision Training",
                        category="GPU",
                        description=(
                            "PyTorch training workload detected."
                        ),
                        reason=(
                            "Mixed precision typically reduces memory usage "
                            "and speeds up GPU training."
                        ),
                        recommendation=(
                            "Benchmark torch.amp.autocast and GradScaler "
                            "during training."
                        ),
                        expected_impact="20-50%",
                        confidence=93,
                        detector="FrameworkRules",
                        priority="High",
                    )
                )

        # --------------------------------------------------
        # PyTorch Inference
        # --------------------------------------------------

        if (
            "pytorch" in frameworks
            and inference
        ):

            opportunities.append(
                OptimizationOpportunity(
                    title="Evaluate torch.compile",
                    category="Inference",
                    description=(
                        "PyTorch inference workload detected."
                    ),
                    reason=(
                        "torch.compile may improve inference performance "
                        "for compatible models."
                    ),
                    recommendation=(
                        "Benchmark torch.compile on representative "
                        "inference workloads before production rollout."
                    ),
                    expected_impact="10-30%",
                    confidence=88,
                    detector="FrameworkRules",
                    priority="Medium",
                )
            )

        # --------------------------------------------------
        # LLM Systems
        # --------------------------------------------------

        llm_stack = {
            "transformers",
            "hugging face",
            "ollama",
            "openai",
        }

        if llm_stack.intersection(frameworks):

            opportunities.append(
                OptimizationOpportunity(
                    title="Optimize LLM Serving",
                    category="LLM",
                    description=(
                        "LLM framework detected."
                    ),
                    reason=(
                        "LLM systems benefit from batching, caching "
                        "and streaming."
                    ),
                    recommendation=(
                        "Evaluate prompt caching, request batching, "
                        "streaming responses and KV-cache reuse."
                    ),
                    expected_impact="15-35%",
                    confidence=91,
                    detector="FrameworkRules",
                    priority="High",
                )
            )

        # --------------------------------------------------
        # FastAPI
        # --------------------------------------------------

        if "fastapi" in frameworks:

            opportunities.append(
                OptimizationOpportunity(
                    title="Optimize FastAPI Throughput",
                    category="Backend",
                    description="FastAPI detected.",
                    reason=(
                        "Async request handling can improve throughput."
                    ),
                    recommendation=(
                        "Profile async endpoints, connection pooling "
                        "and I/O-bound operations."
                    ),
                    expected_impact="10-25%",
                    confidence=87,
                    detector="FrameworkRules",
                    priority="Medium",
                )
            )

        return opportunities