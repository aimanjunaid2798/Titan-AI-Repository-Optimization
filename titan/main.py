"""
main.py

Titan CLI Entry Point.

Author: Titan Team
"""

from __future__ import annotations

import argparse

from titan.analyzer.scanner import RepositoryScanner
from titan.knowledge.builder import KnowledgeBuilder
from titan.llm import OllamaClient
from titan.planner import Planner
from titan.rag import RepositoryRetriever
from titan.report import MarkdownReport
from titan.ui import TitanConsole
from titan.verifier import Verifier


def main():

    console = TitanConsole()

    console.banner()

    parser = argparse.ArgumentParser(
        description="Titan AI Repository Optimizer"
    )

    parser.add_argument(
        "repository",
        help="Path to repository",
    )

    parser.add_argument(
        "--model",
        default="qwen2.5-coder:7b",
        help="Ollama model",
    )

    args = parser.parse_args()

    # --------------------------------------------------
    # Scan Repository
    # --------------------------------------------------

    console.status("Scanning repository...")

    scanner = RepositoryScanner(
        args.repository
    )

    profile = scanner.scan()

    # --------------------------------------------------
    # Build Knowledge
    # --------------------------------------------------

    console.status("Building knowledge...")

    builder = KnowledgeBuilder()

    knowledge = builder.build(
        profile
    )

    # --------------------------------------------------
    # Index Repository Knowledge
    # --------------------------------------------------

    console.status(
        "Indexing repository knowledge..."
    )

    retriever = RepositoryRetriever()

    retriever.index(
        knowledge
    )

    # --------------------------------------------------
    # Initialize AI Components
    # --------------------------------------------------

    llm = OllamaClient(
        model=args.model
    )

    planner = Planner(
        llm,
        retriever,
    )

    verifier = Verifier(
        llm,
        retriever,
    )

    # --------------------------------------------------
    # Generate Initial Roadmap
    # --------------------------------------------------

    console.status(
        "Generating optimization roadmap..."
    )

    roadmap = planner.plan(
        knowledge
    )

    # --------------------------------------------------
    # Verification Loop
    # --------------------------------------------------

    MAX_RETRIES = 2

    verification = None

    for attempt in range(MAX_RETRIES + 1):

        console.status(
            f"Verification Pass {attempt + 1}"
        )

        verification = verifier.verify(
            knowledge,
            roadmap,
        )

        console.status(
            f"Verification Score: {verification.score}"
        )

        roadmap.verification_score = verification.score

        if verification.approved:

            console.status(
                "Roadmap approved."
            )

            break

        if attempt == MAX_RETRIES:

            console.status(
                "Maximum verification attempts reached."
            )

            break

        console.status(
            "Revising roadmap..."
        )

        roadmap = planner.revise(
            knowledge,
            roadmap,
            verification,
        )

    # --------------------------------------------------
    # Generate Report
    # --------------------------------------------------

    report_generator = MarkdownReport()

    report_path = report_generator.generate(
        profile,
        roadmap,
    )

    console.status(
        f"Report saved to {report_path}"
    )

    console.roadmap(
        roadmap
    )


if __name__ == "__main__":
    main()