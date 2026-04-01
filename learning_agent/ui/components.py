"""
UI components — reusable Streamlit components for the multi-agent system.
"""

import streamlit as st


def render_header() -> None:
    """Render the application header with title and description."""
    st.title("🧠 IS Thinkers — Multi-Agent Learning Strategist")
    st.markdown(
        """
        *A multi-agent AI system powered by the wisdom of Machiavelli, Clausewitz,
        Nash, Schelling, Marcus Aurelius, and Yuval Noah Harari.*
        """,
        unsafe_allow_html=False,
    )
    st.divider()


def render_sidebar(memory) -> None:
    """
    Render the sidebar with system information and interaction history.

    Args:
        memory: The Memory instance from the orchestrator.
    """
    with st.sidebar:
        st.header("🏛️ The Thinkers Council")
        st.markdown(
            """
            **Strategists:**
            - ⚔️ Machiavelli
            - 🎯 Clausewitz
            - ♟️ Nash
            - 🔒 Schelling
            - 📚 Jiang Xueqin

            **Philosophers:**
            - 🌿 Marcus Aurelius
            - 🌍 Yuval Noah Harari
            """
        )
        st.divider()

        st.header("🤖 Active Agents")
        st.markdown(
            """
            - 🔵 **Strategist** — Power & game theory
            - 🔬 **Scientist** — Evidence & validation
            - 🔄 **Habit** — Behavioral systems
            - 📄 **Summarizer** — Document intelligence
            """
        )
        st.divider()

        st.header("📊 Routing Logic")
        st.markdown(
            """
            | Mode | Agents |
            |------|--------|
            | Deep Analysis | All 3 |
            | Quick Answer | Strategist |
            | Learning Plan | Habit + Strategist |
            | Document Analysis | Summarizer + Strategist |
            """
        )
        st.divider()

        if memory and len(memory) > 0:
            st.header(f"🧠 Memory ({len(memory)} interactions)")
            recent = memory.get_context(3)
            for i, (inp, _) in enumerate(recent, 1):
                with st.expander(f"Interaction {i}: {inp[:50]}..."):
                    st.text(inp[:200])

        st.divider()
        st.caption("Built with OpenAI GPT-4o-mini · IS Thinkers System")


def render_output_section(output: str) -> None:
    """
    Render the final multi-agent analysis output.

    Args:
        output: Markdown-formatted output from the orchestrator.
    """
    st.markdown("## 📋 Analysis Results")
    st.divider()

    if not output:
        st.info("No output yet. Submit a query to begin.")
        return

    # Split into sections and render each with appropriate styling
    sections = output.split("\n## ")

    for i, section in enumerate(sections):
        if i == 0:
            # First section (header)
            st.markdown(section)
        else:
            section_with_header = "## " + section
            # Use expanders for individual sections to keep UI clean
            header_line = section.split("\n")[0].strip()
            with st.expander(f"📌 {header_line}", expanded=True):
                # Remove the header line and render content
                content = "\n".join(section.split("\n")[1:])
                st.markdown(content)
