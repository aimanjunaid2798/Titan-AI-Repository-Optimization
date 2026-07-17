"""
models.py

Repository RAG models.

Author: Titan Team
"""

from __future__ import annotations

from typing import List

from pydantic import BaseModel, Field


class FileChunk(BaseModel):
    """
    Represents one semantic repository chunk.
    """

    path: str

    language: str

    module_type: str = "Unknown"

    imports: List[str] = Field(default_factory=list)

    classes: List[str] = Field(default_factory=list)

    functions: List[str] = Field(default_factory=list)

    frameworks: List[str] = Field(default_factory=list)

    gpu_features: List[str] = Field(default_factory=list)

    keywords: List[str] = Field(default_factory=list)

    implementation_file: bool = True

    summary: str = ""

    def metadata(self) -> dict:
        """
        Metadata stored alongside embeddings.
        """

        return {
            "path": self.path,
            "language": self.language,
            "module_type": self.module_type,
            "frameworks": ",".join(self.frameworks),
            "implementation_file": self.implementation_file,
            "gpu_features": ",".join(self.gpu_features),
        }

    def to_text(self) -> str:
        """
        Semantic representation used for embeddings.
        """

        return f"""
    Repository File

    Path:
    {self.path}

    Module Type:
    {self.module_type}

    Language:
    {self.language}

    Primary Responsibility:
    {self.summary}

    Frameworks:
    {", ".join(self.frameworks) if self.frameworks else "None"}

    GPU Features:
    {", ".join(self.gpu_features) if self.gpu_features else "None"}

    Imports:
    {", ".join(self.imports) if self.imports else "None"}

    Classes:
    {", ".join(self.classes) if self.classes else "None"}

    Functions:
    {", ".join(self.functions) if self.functions else "None"}

    Keywords:
    {", ".join(self.keywords) if self.keywords else "None"}

    Implementation File:
    {"Yes" if self.implementation_file else "No"}

    This repository file is relevant for:

    - {self.module_type}
    - {"GPU optimization" if self.gpu_features else "General software engineering"}
    - {"Deep learning" if self.frameworks else "General programming"}

    Use this file when searching for implementation details,
    engineering logic, repository architecture,
    or optimization opportunities.
    """