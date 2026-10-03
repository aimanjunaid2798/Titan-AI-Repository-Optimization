"""
Knowledge layer for Titan.

This package converts low-level repository analysis
into high-level engineering knowledge used by Titan's
AI agents.
"""

from .builder import KnowledgeBuilder
from .models import RepositoryKnowledge

__all__ = [
    "KnowledgeBuilder",
    "RepositoryKnowledge",
]