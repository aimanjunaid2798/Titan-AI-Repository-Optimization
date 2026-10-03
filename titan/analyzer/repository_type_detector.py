"""
repository_type_detector.py

Repository type detector.

Author: Titan Team
"""

from __future__ import annotations

from pathlib import Path

from titan.models.analyzer import (
    RepositoryTypeDetectionResult,
)


class RepositoryTypeDetector:

    def __init__(
        self,
        repository_path: Path,
    ):

        self.repository_path = repository_path

    def detect(
        self,
    ) -> RepositoryTypeDetectionResult:

        result = RepositoryTypeDetectionResult()

        python_files = list(
            self.repository_path.rglob("*.py")
        )

        training_keywords = (
            "trainer",
            "fit(",
            "backward(",
            "optimizer",
            "loss.backward",
            "gradscaler",
            "dataloader",
            "epoch",
        )

        inference_keywords = (
            "pipeline(",
            "generate(",
            "predict(",
            "inference",
            "tokenizer",
            "model.generate",
        )

        rag_keywords = (
            "chromadb",
            "faiss",
            "qdrant",
            "pinecone",
            "sentence_transformers",
            "retriever",
            "embedding",
        )

        cli_keywords = (
            "argparse",
            "typer",
            "__main__",
        )

        infra_keywords = (
            "ollama",
            "openai",
            "llm",
            "prompt",
            "planner",
            "verifier",
        )

        for file in python_files:

            try:

                text = file.read_text(
                    encoding="utf-8",
                    errors="ignore",
                ).lower()

            except Exception:
                continue

            if any(
                keyword in text
                for keyword in training_keywords
            ):
                result.training_detected = True

            if any(
                keyword in text
                for keyword in inference_keywords
            ):
                result.inference_detected = True

            if any(
                keyword in text
                for keyword in rag_keywords
            ):
                result.rag_detected = True

            if any(
                keyword in text
                for keyword in cli_keywords
            ):
                result.cli_detected = True

            if any(
                keyword in text
                for keyword in infra_keywords
            ):
                result.ai_infrastructure_detected = True

        return result