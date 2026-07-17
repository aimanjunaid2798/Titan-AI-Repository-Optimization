"""
models.py

Verification models.

Author: Titan Team
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class VerificationIssue(BaseModel):

    issue_type: str

    description: str


class VerificationResult(BaseModel):

    approved: bool

    score: int = Field(
        ge=0,
        le=100,
    )

    summary: str

    feedback: str = ""

    issues: list[VerificationIssue] = Field(
        default_factory=list
    )