"""
prompts.py

Verifier prompts.

Author: Titan Team
"""

from __future__ import annotations

import json

from titan.knowledge import RepositoryKnowledge
from titan.planner.models import OptimizationRoadmap


SYSTEM_PROMPT = """
You are Titan Verifier.

You are a senior AI Software Engineer responsible for
validating optimization roadmaps.

Your ONLY responsibility is to determine whether every
recommendation is supported by the supplied repository
knowledge and retrieved repository context.

Never invent repository facts.

Repository knowledge is the source of truth.

Retrieved repository context contains real repository files.

Only report an issue when supported by evidence.

Validate:

- hallucinated technologies
- hallucinated frameworks
- hallucinated filenames
- unsupported recommendations
- missing deterministic opportunities
- invalid implementation steps
- confidence consistency
- missing JSON fields

Filename Validation Rules

Only report a filename as invalid if it is NOT present
in the supplied repository context.

If you cannot verify a filename,
DO NOT assume it is missing.

Return ONLY valid JSON.

Schema

{
    "approved": true,
    "score": 95,
    "summary": "...",
    "feedback": "...",
    "issues": [
        {
            "issue_type": "...",
            "description": "..."
        }
    ]
}

--------------------------------------------------
Score Rules
--------------------------------------------------

If approved is true:

- score MUST be between 90 and 100.

If approved is false:

- score MUST be less than 90.

Never return score = 0 unless the roadmap is
completely invalid.

The JSON must be internally consistent.

--------------------------------------------------

Do NOT output markdown.

Do NOT output explanations.

The first character must be {

The last character must be }
"""


class VerificationPrompt:

    @staticmethod
    def build(
        knowledge: RepositoryKnowledge,
        roadmap: OptimizationRoadmap,
        retrieved_context: list[dict],
    ):

        user_prompt = f"""
IMPORTANT

You are NOT the planner.

The roadmap below has ALREADY been generated.

DO NOT regenerate it.

DO NOT improve it.

DO NOT rewrite it.

Your ONLY task is to verify it.

Repository

{json.dumps(
    knowledge.model_dump(),
    indent=4,
)}

Retrieved Repository Context

{json.dumps(
    retrieved_context,
    indent=4,
)}

Roadmap To Verify

{json.dumps(
    roadmap.model_dump(),
    indent=4,
)}

Consistency Rules

If approved is true:

- score must be between 90 and 100.

If approved is false:

- score must be below 90.

Return ONLY the verification JSON.

Do NOT regenerate the roadmap.

Do NOT output anything except the verification JSON.
"""

        return (
            SYSTEM_PROMPT.strip(),
            user_prompt,
        )

    @classmethod
    def build_revision(
        cls,
        knowledge,
        roadmap,
        verification,
        retrieved_context,
    ):

        repository = json.dumps(
            knowledge.model_dump(),
            indent=4,
        )

        previous = json.dumps(
            roadmap.model_dump(),
            indent=4,
        )

        issues = json.dumps(
            [
                issue.model_dump()
                for issue in verification.issues
            ],
            indent=4,
        )

        context = json.dumps(
            retrieved_context,
            indent=4,
        )

        user_prompt = f"""
Repository Knowledge

{repository}

Retrieved Repository Context

{context}

Previous Roadmap

{previous}

Verifier Feedback

{verification.feedback}

Issues

{issues}

Revise the roadmap.

Return ONLY valid JSON.

The first character must be {{

The last character must be }}
"""

        return (
            cls.SYSTEM_PROMPT.strip(),
            user_prompt,
        )