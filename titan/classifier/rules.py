"""
rules.py

Repository classification rules.

Author: Titan Team
"""

from __future__ import annotations

from titan.classifier.models import RepositoryType
from titan.models.repository import RepositoryProfile


class ClassificationRules:
    """
    Deterministic repository classification rules.
    """

    @staticmethod
    def classify(
        profile: RepositoryProfile,
    ) -> tuple[list[RepositoryType], list[str]]:

        repository_types = []
        reasoning = []

        technologies = {
            technology.lower()
            for technology in profile.technologies
        }

        frameworks = {
            framework.lower()
            for framework in profile.frameworks
        }

        languages = {
            language.lower()
            for language in profile.languages
        }

        repository_name = profile.repository_name.lower()

        metadata = profile.metadata

        # -----------------------------
        # RAG
        # -----------------------------

        rag_keywords = {
            "chromadb",
            "faiss",
            "qdrant",
            "pinecone",
            "milvus",
            "sentence-transformers",
            "langchain",
            "llamaindex",
        }

        if (
            rag_keywords.intersection(technologies)
            or rag_keywords.intersection(frameworks)
        ):

            repository_types.append(
                RepositoryType.RAG
            )

            reasoning.append(
                "Detected retrieval/vector database technologies."
            )

        # -----------------------------
        # AI Infrastructure
        # -----------------------------

        infra_keywords = {
            "ollama",
            "openai",
            "transformers",
            "hugging face",
        }

        if (
            infra_keywords.intersection(technologies)
            or infra_keywords.intersection(frameworks)
        ):

            repository_types.append(
                RepositoryType.AI_INFRASTRUCTURE
            )

            reasoning.append(
                "Detected LLM infrastructure."
            )

        # -----------------------------
        # CLI
        # -----------------------------

        if (
            "typer" in frameworks
            or "argparse" in technologies
            or "cli" in repository_name
        ):

            repository_types.append(
                RepositoryType.CLI
            )

            reasoning.append(
                "Repository exposes a command-line interface."
            )

        # -----------------------------
        # Training
        # -----------------------------

        training_markers = metadata.get(
            "training_detected",
            False,
        )

        if training_markers:

            repository_types.append(
                RepositoryType.TRAINING
            )

            reasoning.append(
                "Training pipeline detected."
            )

        # -----------------------------
        # Inference
        # -----------------------------

        inference_markers = metadata.get(
            "inference_detected",
            False,
        )

        if inference_markers:

            repository_types.append(
                RepositoryType.INFERENCE
            )

            reasoning.append(
                "Inference pipeline detected."
            )

        # -----------------------------
        # Backend
        # -----------------------------

        if (
            "fastapi" in frameworks
            or "flask" in frameworks
        ):

            repository_types.append(
                RepositoryType.BACKEND
            )

            reasoning.append(
                "Backend framework detected."
            )

        # -----------------------------
        # Library
        # -----------------------------

        if (
            "python" in languages
            and not repository_types
        ):

            repository_types.append(
                RepositoryType.LIBRARY
            )

            reasoning.append(
                "General-purpose Python library."
            )

        if not repository_types:

            repository_types.append(
                RepositoryType.UNKNOWN
            )

            reasoning.append(
                "Unable to classify repository."
            )

        return (
            repository_types,
            reasoning,
        )