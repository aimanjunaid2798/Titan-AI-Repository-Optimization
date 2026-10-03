"""
markdown.py

Markdown report generator for Titan.

Author: Titan Team
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from titan.models.repository import RepositoryProfile
from titan.planner.models import OptimizationRoadmap


class MarkdownReport:
    """
    Generates professional Markdown reports from
    Titan analysis.
    """

    def __init__(
        self,
        output_directory: str = "reports",
    ):

        self.output_directory = Path(
            output_directory
        )

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def generate(
        self,
        profile: RepositoryProfile,
        roadmap: OptimizationRoadmap,
    ) -> Path:

        repository_name = (
            profile.repository_name
            if profile.repository_name
            else "repository"
        )

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = (
            f"{repository_name}_{timestamp}.md"
        )

        report_path = (
            self.output_directory
            / filename
        )

        languages = (
            ", ".join(profile.languages.keys())
            if profile.languages
            else "None Detected"
        )

        frameworks = (
            ", ".join(profile.frameworks)
            if profile.frameworks
            else "None Detected"
        )

        gpu_backends = (
            ", ".join(profile.gpu_backends)
            if profile.gpu_backends
            else "None Detected"
        )

        lines = []

        # =====================================================
        # Header
        # =====================================================

        lines.append("# ⚡ Titan AI Repository Analysis\n\n")

        lines.append(
            f"**Generated:** "
            f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        )

        lines.append("---\n\n")

        # =====================================================
        # Executive Summary
        # =====================================================

        lines.append("## Executive Summary\n\n")

        lines.append(
            "This repository was analyzed using "
            "**Titan AI Repository Optimization Platform**.\n\n"
        )

        lines.append(
            "Titan combines deterministic repository "
            "analysis, semantic Retrieval-Augmented "
            "Generation (RAG), LLM-based planning, "
            "automated verification and iterative "
            "self-correction to generate engineering "
            "optimization recommendations.\n\n"
        )

        lines.append(
            f"**Repository:** "
            f"{profile.repository_name or "Unknown Repository"}\n\n"
        )

        lines.append(
            f"**Location:** "
            f"`{profile.repository_path}`\n\n"
        )

        lines.append(
            f"**Primary Languages:** "
            f"{languages}\n\n"
        )

        lines.append(
            f"**Frameworks:** "
            f"{frameworks}\n\n"
        )

        lines.append(
            f"**GPU Backends:** "
            f"{gpu_backends}\n\n"
        )

        lines.append(
            f"**Overall AI Confidence:** "
            f"{roadmap.overall_confidence:.0f}%\n\n"
        )

        if roadmap.verification_score is not None:
            lines.append(
                f"**Verification Score:** "
                f"{roadmap.verification_score}%\n\n"
            )

        lines.append("---\n\n")

        # =====================================================
        # Repository Statistics
        # =====================================================

        lines.append("## Repository Statistics\n\n")

        lines.append(
            f"- Total Files: "
            f"{profile.statistics.total_files}\n"
        )

        if profile.statistics.total_directories > 0:
            lines.append(
                f"- Total Directories: "
                f"{profile.statistics.total_directories}\n"
            )

        lines.append(
            f"- Total Lines: "
            f"{profile.statistics.total_lines}\n"
        )

        if profile.statistics.largest_file:
            lines.append(
                f"- Largest File: "
                f"{profile.statistics.largest_file}\n"
            )

        lines.append("\n")


        # =====================================================
        # Detected Opportunities
        # =====================================================

        lines.append("## Detected Opportunities\n\n")

        if profile.opportunities:

            for opportunity in profile.opportunities:

                lines.append(
                    f"- **{opportunity.title}** "
                    f"({opportunity.priority})\n"
                )

        else:

            lines.append(
                "No optimization opportunities detected.\n"
            )

        lines.append("\n")

        # =====================================================
        # Optimization Roadmap
        # =====================================================

        lines.append("## Optimization Roadmap\n\n")

        for index, item in enumerate(
            roadmap.recommendations,
            start=1,
        ):

            lines.append(
                f"# Recommendation {index}\n\n"
            )

            lines.append(
                "| Property | Value |\n"
            )

            lines.append(
                "|----------|-------|\n"
            )

            lines.append(
                f"| Title | {item.title} |\n"
            )

            lines.append(
                f"| Expected Impact | "
                f"{item.expected_impact} |\n"
            )

            lines.append(
                f"| Estimated Speedup | "
                f"{item.estimated_speedup} |\n"
            )

            lines.append(
                f"| Difficulty | "
                f"{item.implementation_difficulty} |\n"
            )

            lines.append(
                f"| Confidence | "
                f"{item.confidence:.0f}% |\n\n"
            )

            lines.append(
                "### Description\n\n"
            )

            lines.append(
                f"{item.description}\n\n"
            )

            lines.append(
                "### Engineering Rationale\n\n"
            )

            lines.append(
                f"{item.rationale}\n\n"
            )

            if item.supporting_evidence:

                lines.append(
                    "### Supporting Evidence\n\n"
                )

                for evidence in item.supporting_evidence:

                    lines.append(
                        f"- {evidence}\n"
                    )

                lines.append("\n")

            if item.affected_files:

                lines.append(
                    "### Affected Files\n\n"
                )

                for file in item.affected_files:

                    lines.append(
                        f"- `{file}`\n"
                    )

                lines.append("\n")

            if item.implementation_steps:

                lines.append(
                    "### Implementation Steps\n\n"
                )

                for step in item.implementation_steps:

                    lines.append(
                        f"- {step}\n"
                    )

                lines.append("\n")

            lines.append("---\n\n")

        # =====================================================
        # Footer
        # =====================================================

        lines.append("## Conclusion\n\n")

        lines.append(
            "Titan successfully analyzed the repository "
            "using deterministic static analysis, "
            "semantic Retrieval-Augmented Generation (RAG), "
            "LLM-based planning, automated verification "
            "and iterative self-correction to generate "
            "a prioritized engineering optimization roadmap.\n\n"
        )

        lines.append(
            f"Overall AI Confidence: "
            f"{roadmap.overall_confidence:.0f}%\n"
        )

        if roadmap.verification_score is not None:
            lines.append(
                f"Verification Score: "
                f"{roadmap.verification_score}%\n"
            )

        lines.append("\n")

        lines.append(
            "## Titan Agent Pipeline\n\n"
        )

        lines.append(
            "Repository Scan → "
            "Knowledge Builder → "
            "Semantic RAG → "
            "Planner Agent → "
            "Verifier Agent → "
            "Revision Loop → "
            "Markdown Report\n\n"
        )

        lines.append("---\n\n")

        lines.append(
            "*Generated by **Titan AI Repository "
            "Optimization Platform***\n"
        )

        report_path.write_text(
            "".join(lines),
            encoding="utf-8",
        )

        return report_path