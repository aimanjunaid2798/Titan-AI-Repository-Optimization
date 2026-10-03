"""
planner.py

Titan Planner.

Author: Titan Team
"""

from __future__ import annotations

from pathlib import Path

from titan.knowledge import RepositoryKnowledge
from titan.llm.base import BaseLLMClient

from titan.planner.models import (
    OptimizationRoadmap,
)

from titan.planner.parser import (
    RoadmapParser,
)

from titan.planner.prompts import (
    PromptBuilder,
)

from titan.rag import RepositoryRetriever

def _select_best_files(
    recommendation,
    retrieved_context,
) -> list[str]:

    title = recommendation.title.lower()

    candidates = []

    for item in retrieved_context:

        path = item["path"].replace("\\", "/")

        filename = Path(path).name.lower()

        module = item.get(
            "module_type",
            "",
        ).lower()

        summary = item.get(
            "summary",
            "",
        ).lower()

        imports = " ".join(
            item.get("imports", [])
        ).lower()

        score = item.get(
            "score",
            999,
        )

        # Lower distance = better
        priority = -score

        # ---------------------------------------
        # GPU Recommendations
        # ---------------------------------------

        if any(
            keyword in title
            for keyword in (
                "gpu",
                "cuda",
                "mixed precision",
                "amp",
                "compile",
                "torch",
            )
        ):

            gpu_keywords = (
                "gpu",
                "cuda",
                "amp",
                "autocast",
                "gradscaler",
                "torch",
                "compile",
                "trainer",
                "training",
                "inference",
                "model",
            )

            if any(
                keyword in filename
                for keyword in gpu_keywords
            ):
                priority += 100

            if any(
                keyword in summary
                for keyword in gpu_keywords
            ):
                priority += 80

            if any(
                keyword in imports
                for keyword in (
                    "torch",
                    "torch.cuda",
                )
            ):
                priority += 60

            if module in (
                "training",
                "gpu",
                "model",
                "inference",
            ):
                priority += 80

        # ---------------------------------------
        # Retrieval Recommendations
        # ---------------------------------------

        elif any(
            keyword in title
            for keyword in (
                "retrieval",
                "embedding",
                "vector",
                "index",
            )
        ):

            retrieval_keywords = (
                "retriever",
                "retrieval",
                "embedding",
                "embeddings",
                "vector",
                "index",
                "search",
                "faiss",
                "chroma",
                "chromadb",
                "qdrant",
                "pinecone",
            )

            if any(
                keyword in filename
                for keyword in retrieval_keywords
            ):
                priority += 100

            if any(
                keyword in summary
                for keyword in retrieval_keywords
            ):
                priority += 80

            if module in (
                "retrieval",
                "embedding",
                "vector_store",
                "indexing",
            ):
                priority += 80

        # ---------------------------------------
        # LLM Recommendations
        # ---------------------------------------

        elif any(
            keyword in title
            for keyword in (
                "llm",
                "serving",
                "prompt",
            )
        ):

            llm_keywords = (
                "llm",
                "openai",
                "transformers",
                "vllm",
                "ollama",
                "anthropic",
                "litellm",
                "prompt",
                "chat",
            )

            if any(
                keyword in filename
                for keyword in llm_keywords
            ):
                priority += 100

            if any(
                keyword in summary
                for keyword in llm_keywords
            ):
                priority += 80

        # ---------------------------------------
        # Penalize support modules
        # ---------------------------------------

        if filename in (
            "planner.py",
            "prompts.py",
            "config.py",
            "__init__.py",
        ):
            priority -= 1000

        candidates.append(
            (
                priority,
                path,
            )
        )

    candidates.sort(
        reverse=True
    )

    return [
        path
        for _, path in candidates[:3]
    ]

class Planner:
    """
    Generates optimization roadmaps using
    Repository RAG.
    """

    def __init__(
        self,
        llm: BaseLLMClient,
        retriever: RepositoryRetriever,
    ):

        self.llm = llm
        self.retriever = retriever

    def plan(
        self,
        knowledge: RepositoryKnowledge,
    ) -> OptimizationRoadmap:
        """
        Generate an optimization roadmap.
        """

        # ----------------------------------------
        # Retrieve repository evidence
        # ----------------------------------------

        retrieved_context = (
            self.retriever.retrieve(
                knowledge,
            )
        )

        retrieved_context = sorted(
            retrieved_context,
            key=lambda item: (
                item["score"]
                if item["score"] is not None
                else 999
            ),
        )[:7]

        # ----------------------------------------
        # Build prompt
        # ----------------------------------------

        system_prompt, user_prompt = (
            PromptBuilder.build(
                knowledge,
                retrieved_context,
            )
        )

        # ----------------------------------------
        # Generate roadmap
        # ----------------------------------------

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema=OptimizationRoadmap,
        )

        roadmap = RoadmapParser.parse(
            response
        )

        # ----------------------------------------
        # Post Processing
        # ----------------------------------------

        for recommendation in roadmap.recommendations:

            # ----------------------------
            # Clean affected files
            # ----------------------------

            """cleaned = []

            for file in recommendation.affected_files:

                name = Path(file).name

                if name.endswith(
                    (
                        ".py",
                        ".cpp",
                        ".cu",
                        ".c",
                    )
                ):
                    cleaned.append(name)"""

            recommendation.affected_files = _select_best_files(
                recommendation,
                retrieved_context,
            )

            # ----------------------------
            # Attach supporting evidence
            # ----------------------------

            recommendation.supporting_evidence = []

            for item in retrieved_context:

                if len(recommendation.supporting_evidence) >= 3:
                    break

                evidence = (
                    f"{item['path']} "
                    f"(Module: {item['module_type']}, "
                    f"Frameworks: {item['frameworks'] or 'None'}, "
                    f"GPU: {item['gpu_features'] or 'None'})"
                )

                recommendation.supporting_evidence.append(
                    evidence
                )

            # ----------------------------
            # Dynamic confidence
            # ----------------------------

            confidence = 60

            if recommendation.affected_files:
                confidence += 15

            if recommendation.supporting_evidence:
                confidence += 10

            if recommendation.rationale.strip():
                confidence += 5

            if recommendation.expected_impact.strip():
                confidence += 5

            if recommendation.implementation_steps:
                confidence += 5

            recommendation.confidence = min(
                confidence,
                100,
            )

        # ----------------------------------------
        # Repository name fallback
        # ----------------------------------------

        if (
            not roadmap.repository_name
            or roadmap.repository_name.lower()
            == "unknown repository"
        ):
            roadmap.repository_name = (
                knowledge.repository_name
            )

        # ----------------------------------------
        # Overall confidence
        # ----------------------------------------

        if roadmap.recommendations:

            roadmap.overall_confidence = int(

                sum(
                    recommendation.confidence
                    for recommendation
                    in roadmap.recommendations
                )

                / len(
                    roadmap.recommendations
                )

            )

        else:

            roadmap.overall_confidence = 0

        return roadmap

    def revise(
        self,
        knowledge: RepositoryKnowledge,
        previous_roadmap: OptimizationRoadmap,
        verification,
    ) -> OptimizationRoadmap:
        """
        Revise a roadmap using verifier
        feedback.
        """

        # ----------------------------------------
        # Retrieve repository evidence
        # ----------------------------------------

        retrieved_context = (
            self.retriever.retrieve(
                knowledge,
            )
        )

        retrieved_context = sorted(
            retrieved_context,
            key=lambda item: (
                item["score"]
                if item["score"] is not None
                else 999
            ),
        )[:7]

        # ----------------------------------------
        # Build revision prompt
        # ----------------------------------------

        system_prompt, user_prompt = (
            PromptBuilder.build_revision(
                knowledge,
                previous_roadmap,
                verification,
            )
        )

        # ----------------------------------------
        # Generate revised roadmap
        # ----------------------------------------

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema=OptimizationRoadmap,
        )

        roadmap = RoadmapParser.parse(
            response
        )

        # ----------------------------------------
        # Post Processing (same as plan)
        # ----------------------------------------

        for recommendation in roadmap.recommendations:

            recommendation.affected_files = (
                _select_best_files(
                    recommendation,
                    retrieved_context,
                )
            )

            recommendation.supporting_evidence = []

            for item in retrieved_context:

                if (
                    len(
                        recommendation.supporting_evidence
                    )
                    >= 3
                ):
                    break

                evidence = (
                    f"{item['path']} "
                    f"(Module: {item['module_type']}, "
                    f"Frameworks: {item['frameworks'] or 'None'}, "
                    f"GPU: {item['gpu_features'] or 'None'})"
                )

                recommendation.supporting_evidence.append(
                    evidence
                )

            confidence = 60

            if recommendation.affected_files:
                confidence += 15

            if recommendation.supporting_evidence:
                confidence += 10

            if recommendation.rationale.strip():
                confidence += 5

            if recommendation.expected_impact.strip():
                confidence += 5

            if recommendation.implementation_steps:
                confidence += 5

            recommendation.confidence = min(
                confidence,
                100,
            )

        # ----------------------------------------
        # Repository name fallback
        # ----------------------------------------

        if (
            not roadmap.repository_name
            or roadmap.repository_name.lower()
            == "unknown repository"
        ):
            roadmap.repository_name = (
                knowledge.repository_name
            )

        # ----------------------------------------
        # Overall confidence
        # ----------------------------------------

        if roadmap.recommendations:

            roadmap.overall_confidence = int(
                sum(
                    recommendation.confidence
                    for recommendation
                    in roadmap.recommendations
                )
                / len(
                    roadmap.recommendations
                )
            )

        else:

            roadmap.overall_confidence = 0

        return roadmap