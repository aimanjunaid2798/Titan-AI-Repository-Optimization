import shutil
import tempfile
import zipfile
from pathlib import Path

import streamlit as st

from titan.analyzer.scanner import RepositoryScanner
from titan.knowledge.builder import KnowledgeBuilder
from titan.llm import GroqClient
from titan.planner import Planner
from titan.rag import RepositoryRetriever
from titan.report import MarkdownReport
from titan.verifier import Verifier

st.set_page_config(page_title="Titan AI Repository Optimizer", page_icon="⚙️", layout="wide")

st.title("Titan AI Repository Optimizer")
st.caption("AI-powered repository analysis, optimization planning, and verification.")

api_key = st.secrets.get("GROQ_API_KEY", "")
model = st.secrets.get("GROQ_MODEL", "openai/gpt-oss-120b")

with st.sidebar:
    st.subheader("Titan Configuration")
    st.write(f"**LLM:** `{model}`")
    st.write("**Provider:** Groq")
    if api_key:
        st.success("Groq API key configured")
    else:
        st.error("GROQ_API_KEY is not configured")
        st.info("Add GROQ_API_KEY in Streamlit Cloud → Settings → Secrets.")

uploaded = st.file_uploader(
    "Upload your AI/ML repository as a ZIP",
    type=["zip"],
    help="Upload a repository ZIP. Titan will scan it, build repository knowledge, retrieve evidence, generate an optimization roadmap, and verify it.",
)

if st.button("Analyze Repository", type="primary", disabled=uploaded is None or not api_key):
    work_dir = Path(tempfile.mkdtemp(prefix="titan_"))

    try:
        zip_path = work_dir / "repository.zip"
        zip_path.write_bytes(uploaded.getvalue())

        extract_dir = work_dir / "repo"
        extract_dir.mkdir()

        with zipfile.ZipFile(zip_path) as archive:
            for member in archive.infolist():
                target = (extract_dir / member.filename).resolve()
                if not str(target).startswith(str(extract_dir.resolve()) + "/") and target != extract_dir.resolve():
                    raise ValueError("Unsafe ZIP entry detected.")
            archive.extractall(extract_dir)

        # GitHub ZIPs normally contain one top-level directory.
        children = [p for p in extract_dir.iterdir() if p.name != "__MACOSX"]
        if len(children) == 1 and children[0].is_dir():
            repo_path = children[0]
        else:
            repo_path = extract_dir

        with st.status("Running Titan analysis...", expanded=True) as status:
            st.write("Scanning repository...")
            scanner = RepositoryScanner(str(repo_path))
            profile = scanner.scan()

            st.write("Building repository knowledge...")
            builder = KnowledgeBuilder()
            knowledge = builder.build(profile)

            st.write("Indexing knowledge for RAG retrieval...")
            retriever = RepositoryRetriever()
            retriever.index(knowledge)

            st.write("Generating optimization roadmap with Groq...")
            llm = GroqClient(model=model, api_key=api_key)
            planner = Planner(llm, retriever)
            verifier = Verifier(llm, retriever)
            roadmap = planner.plan(knowledge)

            for attempt in range(3):
                st.write(f"Verification pass {attempt + 1}...")
                verification = verifier.verify(knowledge, roadmap)
                roadmap.verification_score = verification.score

                if verification.approved or attempt == 2:
                    break

                st.write("Roadmap requires refinement; revising...")
                roadmap = planner.revise(knowledge, roadmap, verification)

            report_generator = MarkdownReport()
            report_dir = work_dir / "reports"
            report_dir.mkdir(exist_ok=True)
            report_path = report_generator.generate(profile, roadmap)

            # The report generator writes relative to its configured/default location.
            generated_path = Path(report_path)
            if generated_path.exists():
                report_text = generated_path.read_text(encoding="utf-8")
            else:
                report_text = str(roadmap.model_dump_json(indent=2))

            status.update(label="Titan analysis completed", state="complete")

        st.success("Repository analyzed successfully.")

        col1, col2, col3 = st.columns(3)
        col1.metric("Files", profile.statistics.total_files)
        col2.metric("Recommendations", len(roadmap.recommendations))
        col3.metric("Verification Score", str(getattr(roadmap, "verification_score", "N/A")))

        st.subheader("Optimization Report")
        st.markdown(report_text)
        st.download_button(
            "Download Report",
            report_text,
            file_name="titan_optimization_report.md",
            mime="text/markdown",
        )

    except Exception as exc:
        st.error("Titan execution failed.")
        with st.expander("Developer Logs"):
            st.exception(exc)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
