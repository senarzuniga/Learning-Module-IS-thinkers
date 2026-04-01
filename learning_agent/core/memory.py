"""
Memory module — provides basic session memory for the orchestrator.
"""

from typing import List, Tuple


class Memory:
    """
    Basic in-session memory that stores interaction history and provides
    recent context to agents.
    """

    def __init__(self, max_history: int = 10):
        self.history: List[Tuple[str, str]] = []
        self.max_history = max_history

    def add(self, input_text: str, output: str) -> None:
        """
        Add a new interaction to memory.

        Args:
            input_text: The user's input or query.
            output: The system's full response.
        """
        self.history.append((input_text, output))
        if len(self.history) > self.max_history:
            self.history = self.history[-self.max_history :]

    def get_context(self, n: int = 3) -> List[Tuple[str, str]]:
        """
        Retrieve the last n interactions for context.

        Args:
            n: Number of recent interactions to return (default: 3).

        Returns:
            List of (input, output) tuples.
        """
        return self.history[-n:]

    def format_context(self, n: int = 3) -> str:
        """
        Format recent memory as a readable string for injection into prompts.

        Args:
            n: Number of recent interactions to include.

        Returns:
            Formatted string of recent context.
        """
        recent = self.get_context(n)
        if not recent:
            return ""

        parts = []
        for i, (inp, out) in enumerate(recent, 1):
            parts.append(
                f"[Interaction {i}]\nInput: {inp[:300]}...\nOutput: {out[:500]}..."
            )
        return "\n\n".join(parts)

    def clear(self) -> None:
        """Clear all stored history."""
        self.history = []

    def __len__(self) -> int:
        return len(self.history)
