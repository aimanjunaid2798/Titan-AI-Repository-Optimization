"""
vector_store.py

Persistent ChromaDB wrapper.

Author: Titan Team
"""

from __future__ import annotations

from typing import Any

import chromadb
from chromadb.config import Settings


class VectorStore:
    """
    Thin wrapper around ChromaDB.
    """

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path=".titan_db",
            settings=Settings(
                anonymized_telemetry=False,
            ),
        )

        self.collection = None

    # ---------------------------------------------------------
    # Collection Management
    # ---------------------------------------------------------

    def create_collection(
        self,
        name: str,
    ) -> None:

        self.collection = (
            self.client.get_or_create_collection(
                name=name,
            )
        )

    def set_collection(
        self,
        name: str,
    ) -> None:

        self.collection = (
            self.client.get_or_create_collection(
                name=name,
            )
        )

    def reset_collection(
        self,
        name: str,
    ) -> None:

        try:

            self.client.delete_collection(
                name=name,
            )

        except Exception:
            pass

        self.create_collection(
            name,
        )

    # ---------------------------------------------------------
    # Indexing
    # ---------------------------------------------------------

    def add(
        self,
        chunks: list,
        embeddings: Any,
    ) -> None:

        if self.collection is None:

            raise RuntimeError(
                "Collection has not been created."
            )

        self.collection.add(

            ids=[
                str(i)
                for i in range(
                    len(chunks)
                )
            ],

            documents=[
                chunk.to_text()
                for chunk in chunks
            ],

            metadatas=[
                chunk.metadata()
                for chunk in chunks
            ],

            embeddings=embeddings.tolist(),
        )

    # ---------------------------------------------------------
    # Search
    # ---------------------------------------------------------

    def search(
        self,
        embedding: Any,
        k: int = 5,
        where: dict | None = None,
    ) -> dict:

        if self.collection is None:

            raise RuntimeError(
                "Collection has not been created."
            )

        return self.collection.query(

            query_embeddings=[
                embedding.tolist()
            ],

            n_results=k,

            where=where,
        )

    # ---------------------------------------------------------
    # Utilities
    # ---------------------------------------------------------

    def count(
        self,
    ) -> int:

        if self.collection is None:
            return 0

        return self.collection.count()

    def clear(
        self,
    ) -> None:

        if self.collection is None:
            return

        ids = self.collection.get()["ids"]

        if ids:

            self.collection.delete(
                ids=ids,
            )

    def get_all(
        self,
    ) -> dict:

        if self.collection is None:

            raise RuntimeError(
                "Collection has not been created."
            )

        return self.collection.get()