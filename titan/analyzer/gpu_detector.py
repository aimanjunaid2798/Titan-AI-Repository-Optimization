"""
gpu_detector.py

Detect GPU technologies and optimization features
used inside a repository.

Author: Titan Team
"""

from __future__ import annotations

from pathlib import Path

from titan.config.config_loader import ConfigLoader
from titan.models.analyzer import GPUDetectionResult
from titan.utils.repository_walker import RepositoryWalker


class GPUDetector:
    """
    Detect GPU backends and optimization features
    used inside a repository.
    """

    SUPPORTED_EXTENSIONS = {
        ".py",
        ".cu",
        ".cuh",
        ".cpp",
        ".hpp",
        ".cc",
    }

    GPU_BACKENDS = {
        "CUDA",
        "ROCm",
        "Triton",
        "TensorRT",
    }

    def __init__(
        self,
        repository_path: Path,
    ):

        self.repository_path = repository_path

        self.patterns = ConfigLoader.load(
            "gpu.json"
        )

        self.walker = RepositoryWalker(
            repository_path
        )

    def detect(self) -> GPUDetectionResult:

        detected_backends = set()

        detected_features = set()

        scanned_files = 0

        training_detected = False
        inference_detected = False
        rag_detected = False

        for path in self.walker.iter_files(
            extensions=self.SUPPORTED_EXTENSIONS
        ):

            scanned_files += 1

            content = self.walker.read_text_file(
                path
            )

            source = content.lower()

            # ----------------------------------------
            # Detect GPU technologies
            # ----------------------------------------

            for (
                technology,
                patterns,
            ) in self.patterns.items():

                if any(
                    pattern in content
                    for pattern in patterns
                ):

                    if technology in self.GPU_BACKENDS:

                        detected_backends.add(
                            technology
                        )

                    else:

                        detected_features.add(
                            technology
                        )

            # ----------------------------------------
            # Detect Training
            # ----------------------------------------

            if any(
                keyword in source
                for keyword in (
                    "loss.backward",
                    "backward(",
                    "optimizer.step",
                    "optimizer.zero_grad",
                    "trainingarguments",
                    "trainer(",
                    "trainer =",
                    "gradscaler",
                    "autocast",
                    ".train(",
                    "model.train(",
                )
            ):
                training_detected = True

            # ----------------------------------------
            # Detect Inference
            # ----------------------------------------

            if any(
                keyword in source
                for keyword in (
                    "model.generate",
                    "generate(",
                    "predict(",
                    "pipeline(",
                    "model.eval(",
                    ".eval(",
                    "inference",
                )
            ):
                inference_detected = True

            # ----------------------------------------
            # Detect RAG
            # ----------------------------------------

            if any(
                keyword in source
                for keyword in (
                    "chromadb",
                    "faiss",
                    "qdrant",
                    "pinecone",
                    "milvus",
                    "weaviate",
                    "sentence_transformers",
                    "sentence-transformers",
                    "embedding",
                    "embeddings",
                    "retriever",
                    "vectorstore",
                    "vector_store",
                    "rag",
                )
            ):
                rag_detected = True

        return GPUDetectionResult(

            gpu_backends=sorted(
                detected_backends
            ),

            optimization_features=sorted(
                detected_features
            ),

            training_detected=training_detected,

            inference_detected=inference_detected,

            rag_detected=rag_detected,

            scanned_files=scanned_files,
        )