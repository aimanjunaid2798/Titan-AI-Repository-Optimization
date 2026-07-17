"""
chunker.py

Repository Intelligence Builder.

Author: Titan Team
"""

from __future__ import annotations

import ast
from pathlib import Path

from titan.knowledge import RepositoryKnowledge
from titan.rag.models import FileChunk


FRAMEWORK_KEYWORDS = {
    "torch": "PyTorch",
    "tensorflow": "TensorFlow",
    "keras": "Keras",
    "transformers": "Hugging Face",
    "langchain": "LangChain",
    "langgraph": "LangGraph",
    "fastapi": "FastAPI",
    "flask": "Flask",
    "streamlit": "Streamlit",
    "gradio": "Gradio",
}

GPU_KEYWORDS = {
    "cuda": "CUDA",
    "torch.cuda": "CUDA",
    "autocast": "AMP",
    "gradscaler": "GradScaler",
    "amp": "AMP",
    "fp16": "FP16",
    "bf16": "BF16",
    "torch.compile": "TorchCompile",
    "compile(": "TorchCompile",
    "torch.amp": "AMP",
    "grad_scaler": "GradScaler",
    "device": "CUDA Device",
    "onnx": "ONNX",
    "tensorrt": "TensorRT",
    "openvino": "OpenVINO",
}

SKIP_DIRS = {
    ".venv",
    "venv",
    "__pycache__",
    ".git",
    ".titan_db",
    "site-packages",
    ".pytest_cache",
    ".mypy_cache",
    ".idea",
    ".vscode",
    "build",
    "dist",
}


class KnowledgeChunker:
    """
    Builds semantic repository chunks.
    """

    def _module_type(
        self,
        path: str,
    ) -> str:

        p = path.lower()

        if any(x in p for x in ("gpu", "cuda", "amp")):
            return "GPU"

        if "train" in p:
            return "Training"

        if "infer" in p:
            return "Inference"

        if "model" in p:
            return "Model"

        if "engine" in p:
            return "Engine"

        if "planner" in p:
            return "Planner"

        if "verifier" in p:
            return "Verifier"

        if "rag" in p:
            return "RAG"

        if "llm" in p:
            return "LLM"

        if "knowledge" in p:
            return "Knowledge"

        if "api" in p:
            return "API"

        if "report" in p:
            return "Reporting"

        if "scanner" in p:
            return "Scanner"

        if "test" in p:
            return "Test"

        return "General"

    def chunk(
        self,
        knowledge: RepositoryKnowledge,
    ) -> list[FileChunk]:

        root = Path(
            knowledge.repository_path
        )

        chunks = []

        indexed = 0

        for file in root.rglob("*.py"):

            if any(
                part in SKIP_DIRS
                for part in file.parts
            ):
                continue

            try:

                source = file.read_text(
                    encoding="utf-8"
                )

                tree = ast.parse(source)

            except Exception:
                continue

            imports = set()
            classes = set()
            functions = set()

            frameworks = set()
            gpu_features = set()
            keywords = set()

            for node in ast.walk(tree):

                if isinstance(node, ast.Import):

                    for alias in node.names:
                        imports.add(alias.name)

                elif isinstance(node, ast.ImportFrom):

                    if node.module:
                        imports.add(node.module)

                elif isinstance(node, ast.ClassDef):

                    classes.add(node.name)

                elif isinstance(node, ast.FunctionDef):

                    functions.add(node.name)

            source_lower = source.lower()

            for keyword, framework in FRAMEWORK_KEYWORDS.items():

                if keyword in source_lower:

                    frameworks.add(framework)
                    keywords.add(keyword)

            for keyword, feature in GPU_KEYWORDS.items():

                if keyword in source_lower:

                    gpu_features.add(feature)
                    keywords.add(keyword)

            keywords.update(imports)
            keywords.update(classes)
            keywords.update(functions)

            path_lower = str(file).lower()

            semantic_tags = []

            if any(x in path_lower for x in ("gpu", "cuda", "amp")):
                semantic_tags.extend([
                    "GPU",
                    "CUDA",
                    "Mixed Precision",
                    "Automatic Mixed Precision",
                    "AMP",
                    "Performance",
                ])

            if "planner" in path_lower:
                semantic_tags.extend([
                    "Planning",
                    "Optimization",
                    "Roadmap",
                ])

            if "verifier" in path_lower:
                semantic_tags.extend([
                    "Verification",
                    "Validation",
                ])

            if "rag" in path_lower:
                semantic_tags.extend([
                    "Retrieval",
                    "Embeddings",
                    "Vector Search",
                ])

            if "llm" in path_lower:
                semantic_tags.extend([
                    "Language Model",
                    "Inference",
                ])

            if "knowledge" in path_lower:
                semantic_tags.extend([
                    "Knowledge Graph",
                    "Repository Knowledge",
                ])

            if any(
                keyword in source_lower
                for keyword in (
                    "autocast",
                    "torch.cuda",
                    "gradscaler",
                    "amp",
                    "fp16",
                    "bf16",
                )
            ):
                semantic_tags.extend(
                    [
                        "Mixed Precision",
                        "GPU Acceleration",
                        "Training Optimization",
                    ]
                )

            if gpu_features:

                semantic_tags.extend(
                    [
                        "GPU Implementation",
                        "CUDA Optimization",
                        "Performance Optimization",
                    ]
                )

            if frameworks:

                semantic_tags.extend(frameworks)

            keywords.update(semantic_tags)

            for part in file.parts:
                keywords.add(part.lower())

            module_type = self._module_type(
                str(file.relative_to(root))
            )

            summary = (
                f"Repository File: {file.relative_to(root)}. "
                f"This file implements the {module_type} component of the repository. "
                f"It is responsible for core {module_type.lower()} functionality. "
                f"Frameworks: {', '.join(sorted(frameworks)) if frameworks else 'None'}. "
                f"GPU Features: {', '.join(sorted(gpu_features)) if gpu_features else 'None'}. "
                f"Classes: {', '.join(sorted(classes)) if classes else 'None'}. "
                f"Functions: {', '.join(sorted(functions)) if functions else 'None'}. "
                f"Semantic Tags: {', '.join(sorted(set(semantic_tags))) if semantic_tags else 'None'}."
            )

            path_lower = str(file.relative_to(root)).lower()

            non_implementation_patterns = (
                "query_builder",
                "retriever",
                "prompt",
                "__init__.py",
            )

            implementation_file = not any(
                pattern in path_lower
                for pattern in non_implementation_patterns
            )

            chunk = FileChunk(

                path=str(
                    file.relative_to(root)
                ),

                language="Python",

                module_type=module_type,

                imports=sorted(imports),

                classes=sorted(classes),

                functions=sorted(functions),

                frameworks=sorted(frameworks),

                gpu_features=sorted(gpu_features),

                keywords=sorted(keywords),

                implementation_file=implementation_file,

                summary=summary,
            )

            chunks.append(chunk)

            indexed += 1

        print(
            f"Indexed {indexed} repository files."
        )

        return chunks