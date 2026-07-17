"""
prompts.py

Prompt builder for Titan Planner.

Author: Titan Team
"""

from __future__ import annotations

import json

from titan.knowledge import RepositoryKnowledge


class PromptBuilder:
    """
    Builds prompts for Titan Planner.
    """

    SYSTEM_PROMPT = """
        You are Titan Planner.

        You are a senior AI Software Engineer specializing in:

        - AI infrastructure
        - LLM systems
        - GPU optimization
        - Deep learning
        - High-performance computing
        - Production software engineering
        - Python ecosystems
        - Repository architecture

        Your responsibility is to transform structured repository knowledge into a practical engineering optimization roadmap.

        ==================================================
        GENERAL RULES
        ==================================================

        Use ONLY the supplied repository information.

        Never invent:

        - repositories
        - technologies
        - frameworks
        - dependencies
        - programming languages
        - GPU backends
        - files
        - architecture
        - statistics
        - optimization opportunities

        If information is unavailable, state that it is unavailable.

        Do NOT guess.

        Prefer fewer high-quality recommendations over many speculative ones.

        Prioritize recommendations using engineering ROI.

        Focus on:

        - performance
        - scalability
        - maintainability
        - reliability
        - GPU efficiency
        - inference optimization
        - training optimization
        - engineering best practices

        ==================================================
        REPOSITORY KNOWLEDGE
        ==================================================

        The supplied repository knowledge may contain:

        - repository_name
        - repository_statistics
        - languages
        - frameworks
        - gpu_backends
        - technologies
        - optimization_targets
        - opportunities
        - repository_summary

        Treat every field as factual.

        Do not contradict deterministic repository analysis.

        ==================================================
        DETERMINISTIC OPPORTUNITIES
        ==================================================

        The supplied opportunities are produced by Titan's
        deterministic Opportunity Engine.

        Treat these opportunities as the primary source of
        recommendations.

        Your responsibility is NOT to invent opportunities.

        Instead, expand deterministic opportunities into
        high-quality engineering recommendations.

        Only create a new recommendation if it is directly
        supported by the supplied repository knowledge.

        ==================================================
        RETRIEVED REPOSITORY EVIDENCE
        ==================================================

        The planner will receive retrieved repository evidence.

        Each evidence item represents a REAL repository file.

        Every recommendation MUST be grounded in one or more
        retrieved repository files.

        Planning Algorithm

        For every recommendation:

        Step 1
        Select the retrieved implementation file.

        Step 2
        Explain why that file is relevant.

        Step 3
        Generate the recommendation around that file.

        Step 4
        Populate affected_files using ONLY those files.

        Never reverse this order.

        Never generate a recommendation first and then search
        for affected files.

        ==================================================
        OUTPUT FORMAT
        ==================================================

        Return EXACTLY one valid JSON object.

        Do NOT write:

        - markdown
        - explanations
        - notes
        - comments
        - code fences
        - introductory text
        - concluding text

        Your response MUST begin with:

        {

        and MUST end with:

        }

        Anything outside the JSON object is invalid.

        ==================================================
        JSON SCHEMA
        ==================================================

        {
            "repository_name": "string",
            "summary": "string",
            "recommendations": [
                {
                    "priority": 1,
                    "title": "string",
                    "description": "string",
                    "rationale": "string",
                    "expected_impact": "string",
                    "estimated_speedup": "Estimated",
                    "implementation_difficulty": "Low",
                    "affected_files": [],
                    "implementation_steps": [
                        "step 1",
                        "step 2",
                        "step 3"
                    ],
                    "confidence": 95
                }
            ],
            "overall_confidence": 92
        }

        ==================================================
        RECOMMENDATION RULES
        ==================================================

        Every recommendation MUST include

        - priority
        - title
        - description
        - rationale
        - expected_impact
        - estimated_speedup
        - implementation_difficulty
        - affected_files
        - implementation_steps
        - confidence

        Every recommendation MUST be directly supported by
        retrieved repository evidence.

        Every recommendation MUST reference at least one
        retrieved implementation file.

        The recommendation MUST describe improvements to the
        selected retrieved file.

        Never create a recommendation that is unrelated to
        the selected evidence.

        If multiple retrieved files contribute to the same
        recommendation, include all of them.

        If no retrieved implementation file supports a
        deterministic opportunity, do NOT generate that
        recommendation.

        ==================================================
        AFFECTED FILES
        ==================================================

        affected_files MUST contain ONLY filenames appearing
        inside Retrieved Repository Evidence.

        Never

        - invent filenames
        - infer filenames
        - rename files
        - shorten paths incorrectly
        - guess implementation files

        Do NOT use

        - prompts.py
        - config.py
        - settings.py
        - __init__.py

        unless the retrieved repository evidence explicitly
        shows they implement the detected opportunity.

        If no implementation file supports the
        recommendation

        "affected_files": []

        ==================================================
        IMPLEMENTATION STEPS
        ==================================================

        Provide between 3 and 5 concise engineering steps.

        Each step should be:

        - actionable
        - implementation-focused
        - repository-independent
        - technically accurate

        Avoid mentioning filenames unless they are explicitly
        provided.

        ==================================================
        EXPECTED IMPACT
        ==================================================

        Describe expected engineering improvements such as:

        - lower latency
        - reduced GPU memory usage
        - higher throughput
        - lower inference cost
        - improved maintainability
        - improved scalability

        ==================================================
        ESTIMATED SPEEDUP
        ==================================================

        Never invent benchmark numbers.

        If repository information is insufficient:

        "estimated_speedup": "Estimated"

        Otherwise provide conservative ranges such as:

        - "5-10%"
        - "10-20%"
        - "20-30%"

        ==================================================
        CONFIDENCE
        ==================================================

        Confidence represents confidence in the recommendation,
        NOT expected performance improvement.

        Use:

        95-100
        Strong deterministic evidence.

        80-94
        Multiple supporting indicators.

        60-79
        Some supporting evidence.

        Below 60
        Weak evidence.

        ==================================================
        SUMMARY
        ==================================================

        The summary should:

        - describe the repository
        - mention detected technologies
        - mention major optimization themes
        - be concise
        - not exceed 80 words

        Do not invent missing technologies.

        ==================================================
        ENGINEERING PRIORITY
        ==================================================

        Always prefer implementation modules over support
        modules.

        Priority order

        1. GPU implementation
        2. Training / inference modules
        3. Model implementation
        4. Repository core logic
        5. Utilities
        6. Configuration
        7. Prompt files

        Prompt files should almost never appear inside
        affected_files.

        If both a GPU implementation file and a prompt file
        are retrieved, always choose the GPU implementation
        file.

        Retrieved repository evidence is ordered by semantic
        relevance.

        Earlier evidence is more relevant than later
        evidence.

        Prefer higher-ranked evidence unless a lower-ranked
        file provides substantially stronger implementation
        support.

        ==================================================
        FINAL RESPONSIBILITY
        ==================================================

        Think like a senior AI Software Engineer.

        Do not generate generic advice.

        Produce recommendations that are practical,
        implementation-oriented, technically accurate,
        and directly supported by the supplied repository
        knowledge and deterministic opportunities.
        """

    @classmethod
    def build(
        cls,
        knowledge: RepositoryKnowledge,
        retrieved_context: list[dict],
    ) -> tuple[str, str]:
        """
        Build the planner prompt using repository
        knowledge and retrieved repository evidence.
        """

        repository = {

            "repository_name": knowledge.repository_name,

            "languages": knowledge.languages,

            "frameworks": knowledge.frameworks,

            "gpu_backends": knowledge.gpu_backends,

            "technologies": knowledge.technologies,

            "statistics": knowledge.statistics.model_dump(),

            "optimization_targets":
                knowledge.optimization_targets,

            "risks": knowledge.risks,

            "opportunities": [

                opportunity.model_dump()

                for opportunity

                in knowledge.opportunities
            ],
        }

        # --------------------------------------------------
        # Build structured repository evidence
        # --------------------------------------------------

        evidence_blocks = []

        available_files = []

        for index, item in enumerate(
            retrieved_context,
            start=1,
        ):

            filename = (
                item["path"]
                .replace("\\", "/")
                .split("/")[-1]
            )

            available_files.append(
                f"- {filename}"
            )

            evidence_blocks.append(
                f"""
    Evidence #{index}

    File
    {filename}

    Full Path
    {item["path"]}

    Module Type
    {item["module_type"]}

    Frameworks
    {item["frameworks"] or "None"}

    GPU Features
    {item["gpu_features"] or "None"}

    Summary
    {item["summary"]}

    --------------------------------------------------
    """
            )

        rag_context = "\n".join(
            evidence_blocks
        )

        available_files = "\n".join(
            available_files
        )

        # --------------------------------------------------
        # User Prompt
        # --------------------------------------------------

        user_prompt = f"""
    Repository Knowledge

    {json.dumps(repository, indent=4)}

    ==================================================

    Retrieved Repository Evidence

    The following repository files were retrieved using
    semantic search.

    They are ranked from MOST relevant to LEAST relevant.

    These are REAL repository implementation files.

    {rag_context}

    ==================================================

    Available Evidence Files

    {available_files}

    ==================================================

    Planning Rules

    Repository Knowledge is the primary source of truth.

    Retrieved Repository Evidence is the ONLY valid source
    for affected_files.

    Every recommendation MUST be grounded in one or more
    retrieved repository files.

    Planning Algorithm

    1. Select the retrieved implementation file.

    2. Explain why that file is relevant.

    3. Build the recommendation around that file.

    4. Populate affected_files.

    Never reverse this order.

    Never generate a recommendation first and then guess
    affected_files.

    affected_files MUST contain ONLY filenames listed in
    Available Evidence Files.

    Never invent

    - filenames
    - frameworks
    - technologies
    - modules
    - dependencies

    Never recommend

    - prompts.py
    - config.py
    - settings.py
    - __init__.py

    unless the retrieved evidence explicitly shows they
    implement the detected opportunity.

    If multiple retrieved files contribute to the same
    recommendation, include all of them.

    If no retrieved implementation file supports a
    deterministic opportunity, DO NOT generate that
    recommendation.

    Generate a prioritized optimization roadmap.
    """

        return (
            cls.SYSTEM_PROMPT.strip(),
            user_prompt,
        )

    @classmethod
    def build_revision(
        cls,
        knowledge: RepositoryKnowledge,
        previous_roadmap,
        verification,
    ) -> tuple[str, str]:
        """
        Build a prompt for revising an optimization
        roadmap using verifier feedback.
        """

        repository = json.dumps(
            knowledge.model_dump(),
            indent=4,
        )

        roadmap = json.dumps(
            previous_roadmap.model_dump(),
            indent=4,
        )

        issues = json.dumps(
            [
                issue.model_dump()
                for issue in verification.issues
            ],
            indent=4,
        )

        user_prompt = f"""
    Repository Knowledge

    {repository}

    ==================================================

    Previous Optimization Roadmap

    {roadmap}

    ==================================================

    Verifier Summary

    {verification.summary}

    Verifier Feedback

    {verification.feedback}

    Issues

    {issues}

    ==================================================

    TASK

    Revise the EXISTING optimization roadmap.

    Do NOT generate a completely new roadmap.

    Preserve every valid recommendation.

    Only modify recommendations affected by the verifier
    feedback.

    Remove unsupported recommendations.

    Correct hallucinated

    - filenames
    - frameworks
    - technologies
    - implementation steps

    Do NOT invent new repository facts.

    Repository Knowledge is the only source of truth.

    ==================================================

    OUTPUT

    Return EXACTLY one valid JSON object matching the
    OptimizationRoadmap schema.

    Return NOTHING except the JSON object.

    The FIRST character must be {{

    The LAST character must be }}
    """

        return (
            cls.SYSTEM_PROMPT.strip(),
            user_prompt,
        )