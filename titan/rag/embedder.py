"""
embedder.py

Sentence Transformer embeddings.

Author: Titan Team
"""

from __future__ import annotations

import torch

from sentence_transformers import SentenceTransformer


class EmbeddingModel:
    """
    Repository embedding model.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
    ):

        device = (
            "cuda"
            if torch.cuda.is_available()
            else "cpu"
        )

        self.model = SentenceTransformer(
            model_name,
            device=device,
        )

    def encode_documents(
        self,
        texts: list[str],
    ):
        """
        Encode repository documents.
        """

        texts = [
            (
                "Represent this software repository file "
                "for semantic retrieval.\n\n"
                f"{text}"
            )
            for text in texts
        ]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    def encode_queries(
        self,
        texts: list[str],
    ):
        """
        Encode repository search queries.
        """

        texts = [
            (
                "Represent this repository search query.\n\n"
                f"{text}"
            )
            for text in texts
        ]

        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        )

    # Backward compatibility
    def encode(
        self,
        texts: list[str],
    ):
        """
        Default encoding.
        """

        return self.encode_documents(
            texts
        )