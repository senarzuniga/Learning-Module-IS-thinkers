"""
Orchestrator — the central brain that coordinates all specialized agents.
"""

from typing import Dict, Optional

from ..agents.base_agent import BaseAgent
from ..agents.strategist_agent import StrategistAgent
from ..agents.scientist_agent import ScientistAgent
from ..agents.habit_agent import HabitAgent
from ..agents.summarizer_agent import SummarizerAgent
from .memory import Memory

ROUTING_MAP: Dict[str, list] = {
    "deep_analysis": ["strategist", "scientist", "habit"],
    "quick_answer": ["strategist"],
    "learning_plan": ["habit", "strategist"],
    "document_analysis": ["summarizer", "strategist"],
}

SECTION_LABELS = [
    "1. Core Insight",
    "2. Strategic Breakdown",
    "3. Behavioral System",
    "4. Evidence & Truth Level",
    "5. Macro Perspective",
    "6. Stoic Guidance",
    "7. Action Plan",
]


class Orchestrator:
    """
    Central orchestrator that routes user input to specialized agents,
    coordinates their execution, and merges results into a unified output.
    """

    def __init__(self, agents: Optional[Dict[str, BaseAgent]] = None):
        if agents is not None:
            self.agents = agents
        else:
            self.agents = {
                "strategist": StrategistAgent(),
                "scientist": ScientistAgent(),
                "habit": HabitAgent(),
                "summarizer": SummarizerAgent(),
            }
        self.memory = Memory()

    def route(self, input_text: str, mode: str) -> list:
        """
        Determine which agents to invoke based on the selected mode.

        Args:
            input_text: User input (used for future dynamic routing).
            mode: Analysis mode key.

        Returns:
            Ordered list of agent keys to invoke.
        """
        return ROUTING_MAP.get(mode, ROUTING_MAP["deep_analysis"])

    def execute(
        self,
        input_text: str,
        file_content: str = "",
        mode: str = "deep_analysis",
    ) -> str:
        """
        Run the full multi-agent pipeline for the given input and mode.

        Args:
            input_text: The user's query or thought. May be empty if file_content is provided.
            file_content: Extracted text from an uploaded file (if any). When provided
                          alongside an empty input_text, the document is analyzed directly.
            mode: Analysis mode — controls which agents are invoked.
                  Falls back to 'deep_analysis' for unrecognised modes.

        Returns:
            Structured, merged output from all relevant agents.
        """
        context = self.memory.format_context()
        agent_keys = self.route(input_text, mode)

        agent_outputs: Dict[str, str] = {}

        # If a file was uploaded, run the summarizer first regardless of mode
        if file_content:
            summarizer: SummarizerAgent = self.agents["summarizer"]
            summary = summarizer.run(file_content, context)
            agent_outputs["summarizer"] = summary
            # Augment the input text with the document summary
            augmented_input = (
                f"{input_text}\n\n[Document Summary]\n{summary}"
                if input_text.strip()
                else summary
            )
        else:
            augmented_input = input_text

        # Run each routed agent (skip summarizer if already run)
        for key in agent_keys:
            if key == "summarizer" and "summarizer" in agent_outputs:
                continue
            agent = self.agents.get(key)
            if agent:
                agent_outputs[key] = agent.run(augmented_input, context)

        # Merge all outputs into a structured final response
        final_output = self._merge_outputs(
            input_text=input_text,
            mode=mode,
            agent_outputs=agent_outputs,
            file_content=file_content,
        )

        self.memory.add(input_text, final_output)
        return final_output

    def _merge_outputs(
        self,
        input_text: str,
        mode: str,
        agent_outputs: Dict[str, str],
        file_content: str,
    ) -> str:
        """
        Combine agent outputs into a single structured response.

        Args:
            input_text: Original user input.
            mode: Analysis mode used.
            agent_outputs: Dictionary of agent name → output string.
            file_content: Whether a file was processed.

        Returns:
            Final merged output string.
        """
        sections = []

        # Header
        mode_label = mode.replace("_", " ").title()
        sections.append(f"# 🧠 Multi-Agent Analysis — {mode_label}\n")
        sections.append(f"**Query:** {input_text[:200]}{'...' if len(input_text) > 200 else ''}\n")
        if file_content:
            sections.append("**Document:** ✅ Processed\n")
        sections.append("---\n")

        # Section 1: Core Insight (synthesized from all outputs)
        sections.append("## 1. Core Insight\n")
        if "summarizer" in agent_outputs:
            doc_report = agent_outputs["summarizer"]
            # Extract the one-line summary if present
            one_line = _extract_section(doc_report, "One-Line Summary")
            core_thesis = _extract_section(doc_report, "Core Thesis")
            if core_thesis:
                sections.append(f"**Document Core Thesis:** {core_thesis}\n")
            if one_line:
                sections.append(f"**In One Line:** {one_line}\n")
        else:
            sections.append(
                "_The core insight emerges from the convergence of all agent analyses below._\n"
            )

        # Section 2: Strategic Breakdown
        if "strategist" in agent_outputs:
            sections.append("## 2. Strategic Breakdown\n")
            sections.append(agent_outputs["strategist"])
            sections.append("\n")

        # Section 3: Behavioral System
        if "habit" in agent_outputs:
            sections.append("## 3. Behavioral System\n")
            sections.append(agent_outputs["habit"])
            sections.append("\n")

        # Section 4: Evidence & Truth Level
        if "scientist" in agent_outputs:
            sections.append("## 4. Evidence & Truth Level\n")
            sections.append(agent_outputs["scientist"])
            sections.append("\n")

        # Section 5: Macro Perspective (document intelligence)
        if "summarizer" in agent_outputs:
            sections.append("## 5. Document Intelligence\n")
            sections.append(agent_outputs["summarizer"])
            sections.append("\n")

        # Section 6: Stoic Guidance
        sections.append("## 6. Stoic Guidance (Marcus Aurelius)\n")
        sections.append(
            "_\"You have power over your mind — not outside events. "
            "Realize this, and you will find strength.\"_\n\n"
            "**What is within your control:** Focus on your decisions, "
            "responses, and daily actions.\n\n"
            "**What is outside your control:** Others' reactions, market conditions, "
            "and unforeseen events — accept these with equanimity.\n"
        )

        # Section 7: Action Plan
        sections.append("## 7. Action Plan\n")
        action_items = _extract_action_items(agent_outputs)
        if action_items:
            sections.append(action_items)
        else:
            sections.append(
                "Based on the analysis above:\n"
                "1. Identify the single most important strategic lever\n"
                "2. Design one atomic habit to build momentum\n"
                "3. Validate your assumptions with evidence\n"
                "4. Execute for 30 days, then review\n"
            )

        sections.append("\n---\n")
        sections.append(
            f"_Analysis powered by {len(agent_outputs)} specialized agent(s): "
            f"{', '.join(agent_outputs.keys())}_"
        )

        return "\n".join(sections)


def _extract_section(text: str, section_name: str) -> str:
    """Extract a named section from structured agent output."""
    lines = text.split("\n")
    for i, line in enumerate(lines):
        if section_name.lower() in line.lower():
            # Return the content on the same line or the next non-empty line
            rest = line.split(":", 1)[-1].strip()
            if rest:
                return rest
            for j in range(i + 1, min(i + 5, len(lines))):
                if lines[j].strip():
                    return lines[j].strip()
    return ""


def _extract_action_items(agent_outputs: Dict[str, str]) -> str:
    """Try to extract action items from strategist or habit agent outputs."""
    for key in ["strategist", "habit", "scientist"]:
        if key in agent_outputs:
            text = agent_outputs[key]
            for marker in [
                "Action Plan",
                "Recommendation",
                "Actionable",
                "Implementation",
                "Roadmap",
            ]:
                section = _extract_section(text, marker)
                if section and len(section) > 20:
                    return section
    return ""
