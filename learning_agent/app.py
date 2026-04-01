"""
IS Thinkers — Multi-Agent Learning Strategist System
Main Streamlit application entry point.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

import streamlit as st

from learning_agent.core.orchestrator import Orchestrator
from learning_agent.tools.file_handler import extract_file_content
from learning_agent.tools.voice_handler import transcribe_audio
from learning_agent.ui.components import render_header, render_sidebar, render_output_section

# ── Page configuration (must be the first Streamlit call) ─────────────────────
st.set_page_config(
    page_title="IS Thinkers — Multi-Agent Learning Strategist",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize session state ───────────────────────────────────────────────────
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = Orchestrator()

if "last_output" not in st.session_state:
    st.session_state.last_output = ""

if "is_analyzing" not in st.session_state:
    st.session_state.is_analyzing = False

orchestrator: Orchestrator = st.session_state.orchestrator

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("🧠 IS Thinkers — Multi-Agent Learning Strategist")
st.markdown(
    "*A multi-agent AI system powered by the wisdom of Machiavelli, Clausewitz, "
    "Nash, Schelling, Marcus Aurelius, and Yuval Noah Harari.*"
)
st.divider()

# ── Sidebar ────────────────────────────────────────────────────────────────────
render_sidebar(orchestrator.memory)

# ── Main layout: two columns ───────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.header("📥 Input")

    # Mode selector
    mode = st.selectbox(
        "🎯 Analysis Mode",
        options=["deep_analysis", "quick_answer", "learning_plan", "document_analysis"],
        format_func=lambda x: {
            "deep_analysis": "🔍 Deep Analysis (Strategist + Scientist + Habit)",
            "quick_answer": "⚡ Quick Answer (Strategist only)",
            "learning_plan": "📚 Learning Plan (Habit + Strategist)",
            "document_analysis": "📄 Document Analysis (Summarizer + Strategist)",
        }[x],
        help="Select the analysis depth and which agents are activated.",
    )

    # Text input
    user_input = st.text_area(
        "💭 Your Thought, Problem, or Question",
        height=150,
        placeholder=(
            "Example: 'I don't know how to prioritize my career decisions' or "
            "'Is intermittent fasting effective?' or "
            "'How do I negotiate a salary raise?'"
        ),
    )

    # File upload
    uploaded_file = st.file_uploader(
        "📎 Upload a Document (optional)",
        type=["pdf", "txt"],
        help="Upload a PDF or TXT file. The Summarizer agent will extract key insights.",
    )

    # Voice input
    audio_file = st.file_uploader(
        "🎙️ Upload Voice Input (optional)",
        type=["mp3", "mp4", "wav", "m4a", "webm"],
        key="voice_upload",
        help="Upload an audio file. It will be transcribed and added to your query.",
    )

    # Analyze button
    analyze_clicked = st.button(
        "🚀 Analyze",
        type="primary",
        use_container_width=True,
        disabled=st.session_state.is_analyzing,
    )

    # API key warning
    if not os.getenv("OPENAI_API_KEY"):
        st.warning(
            "⚠️ **OPENAI_API_KEY not set.** "
            "Please set it in your `.env` file or environment variables.",
            icon="⚠️",
        )

    # Clear memory button
    if st.button("🗑️ Clear Memory", use_container_width=True):
        orchestrator.memory.clear()
        st.session_state.last_output = ""
        st.success("Memory cleared.")
        st.rerun()

# ── Analysis Execution ─────────────────────────────────────────────────────────
if analyze_clicked:
    # Collect all inputs
    final_input = user_input.strip()
    file_content = ""
    transcription = ""

    # Process voice input
    if audio_file is not None:
        with st.spinner("🎙️ Transcribing audio..."):
            try:
                audio_bytes = audio_file.read()
                transcription = transcribe_audio(
                    audio_bytes=audio_bytes,
                    filename=audio_file.name,
                )
                if transcription:
                    if final_input:
                        final_input = f"{final_input}\n\n[Voice Transcription]: {transcription}"
                    else:
                        final_input = transcription
                    st.success(f"✅ Audio transcribed: *{transcription[:100]}...*")
            except Exception as e:
                st.error(f"❌ Audio transcription failed: {e}")

    # Process file upload
    if uploaded_file is not None:
        with st.spinner("📄 Extracting document content..."):
            try:
                file_bytes = uploaded_file.read()
                file_content = extract_file_content(
                    file_bytes=file_bytes,
                    filename=uploaded_file.name,
                )
                st.success(f"✅ Document processed: {uploaded_file.name}")
            except Exception as e:
                st.error(f"❌ File extraction failed: {e}")

    # Validate we have something to analyze
    if not final_input and not file_content:
        st.warning("⚠️ Please enter a question, upload a file, or provide audio input.")
    elif not os.getenv("OPENAI_API_KEY"):
        st.error("❌ OPENAI_API_KEY is not configured. Cannot run analysis.")
    else:
        # Run the multi-agent orchestrator
        with col_output:
            with st.spinner("🤖 Multi-agent analysis in progress..."):
                try:
                    output = orchestrator.execute(
                        input_text=final_input or "[Document analysis requested]",
                        file_content=file_content,
                        mode=mode,
                    )
                    st.session_state.last_output = output
                except Exception as e:
                    st.session_state.last_output = ""
                    st.error(f"❌ Analysis failed: {e}")

        st.rerun()

# ── Output Panel ───────────────────────────────────────────────────────────────
with col_output:
    st.header("📤 Analysis Output")

    if st.session_state.last_output:
        render_output_section(st.session_state.last_output)

        # Download button for the analysis
        st.download_button(
            label="⬇️ Download Analysis",
            data=st.session_state.last_output,
            file_name="is_thinkers_analysis.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info(
            "👈 Enter your query on the left and click **Analyze** to begin.\n\n"
            "The multi-agent system will coordinate specialized agents to provide "
            "deep, structured analysis."
        )

        # Show example queries
        with st.expander("💡 Example Queries"):
            st.markdown(
                """
                **Strategic Thinking:**
                > "I don't know how to prioritize my career decisions"

                **Scientific Question:**
                > "Is intermittent fasting effective for weight loss?"

                **Learning Plan:**
                > "I want to learn data science in 6 months while working full-time"

                **Negotiation:**
                > "How do I negotiate a 30% salary increase at my next performance review?"

                **Business Strategy:**
                > "My startup is losing market share to a better-funded competitor"
                """
            )
