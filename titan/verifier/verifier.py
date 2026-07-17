"""
verifier.py

Verification models.

Author: Titan Team
"""


from __future__ import annotations

from titan.knowledge import RepositoryKnowledge

from titan.llm.base import BaseLLMClient

from titan.planner.models import (
    OptimizationRoadmap,
)

from titan.rag import (
    RepositoryRetriever,
)

from titan.verifier.parser import (
    VerificationParser,
)

from titan.verifier.prompts import (
    VerificationPrompt,
)

from titan.verifier.models import (
    VerificationResult,
)


class Verifier:

    def __init__(
        self,
        llm: BaseLLMClient,
        retriever: RepositoryRetriever,
    ):

        self.llm = llm
        self.retriever = retriever

    def verify(
        self,
        knowledge: RepositoryKnowledge,
        roadmap: OptimizationRoadmap,
    ) -> VerificationResult:
        """
        Verify roadmap against repository
        knowledge.
        """

        retrieved_context = (
            self.retriever.retrieve(
                knowledge
            )
        )

        system_prompt, user_prompt = (
            VerificationPrompt.build(
                knowledge,
                roadmap,
                retrieved_context,
            )
        )

        response = self.llm.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            schema=VerificationResult,
        )

        return VerificationParser.parse(
            response
        )