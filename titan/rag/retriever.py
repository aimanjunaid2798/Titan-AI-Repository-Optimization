"""
retriever.py

Repository RAG Retriever.

Author: Titan Team
"""

from __future__ import annotations

from titan.knowledge import RepositoryKnowledge

from titan.rag.chunker import (
    KnowledgeChunker,
)

from titan.rag.embedder import (
    EmbeddingModel,
)

from titan.rag.vector_store import (
    VectorStore,
)

from titan.rag.query_builder import (
    RetrievalQueryBuilder,
)


class RepositoryRetriever:
    """
    Handles indexing and semantic retrieval
    of repository knowledge.
    """

    def __init__(self):

        self.chunker = KnowledgeChunker()

        self.embedder = EmbeddingModel()

        self.store = VectorStore()

        self.query_builder = (
            RetrievalQueryBuilder()
        )

        self._indexed = False

        self.collection_name = None

    def index(
        self,
        knowledge: RepositoryKnowledge,
    ) -> None:
        """
        Index the repository exactly once.
        """

        if self._indexed:
            return

        chunks = self.chunker.chunk(
            knowledge
        )

        if not chunks:
            return

        embeddings = self.embedder.encode_documents(
            [
                chunk.to_text()
                for chunk in chunks
            ]
        )

        self.collection_name = (
            f"repo_{knowledge.repository_name.lower()}"
        )

        self.store.reset_collection(
            self.collection_name
        )

        self.store.add(
            chunks,
            embeddings,
        )

        self._indexed = True

    def retrieve(
        self,
        knowledge: RepositoryKnowledge,
        k: int = 5,
    ) -> list[dict]:
        """
        Retrieve structured repository evidence.
        """

        if not self._indexed:
            raise RuntimeError(
                "Repository has not been indexed."
            )

        queries = self.query_builder.build(
            knowledge
        )

        total = self.store.count()

        if total == 0:
            return []

        aggregated = {}

        for query in queries:

            embedding = self.embedder.encode_queries(
                [query]
            )[0]

            result = self.store.search(
                embedding,
                k=min(max(k * 2, 10), total),
            )

            documents = result.get(
                "documents",
                [],
            )

            metadatas = result.get(
                "metadatas",
                [],
            )

            distances = result.get(
                "distances",
                [],
            )

            if not documents:
                continue

            docs = documents[0]

            metas = (
                metadatas[0]
                if metadatas
                else [{}] * len(docs)
            )

            scores = (
                distances[0]
                if distances
                else [999] * len(docs)
            )

            for doc, meta, score in zip(
                docs,
                metas,
                scores,
            ):

                path = meta.get(
                    "path",
                    doc,
                )

                if (
                    path not in aggregated
                    or score < aggregated[path]["score"]
                ):

                    aggregated[path] = {
                        "path": path,
                        "module_type": meta.get(
                            "module_type",
                            "Unknown",
                        ),
                        "frameworks": meta.get(
                            "frameworks",
                            "",
                        ),
                        "gpu_features": meta.get(
                            "gpu_features",
                            "",
                        ),
                        "implementation_file": meta.get(
                            "implementation_file",
                            True,
                        ),
                        "summary": doc,
                        "score": score,
                    }

        implementation = []
        support = []

        for item in aggregated.values():

            if item.get("implementation_file", True):
                implementation.append(item)
            else:
                support.append(item)

        implementation.sort(key=lambda x: x["score"])
        support.sort(key=lambda x: x["score"])

        retrieved = implementation[:k] + support[:2]

        return retrieved