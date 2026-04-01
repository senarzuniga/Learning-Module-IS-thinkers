"""
Base agent class for all specialized agents in the multi-agent system.
"""

import os
from openai import OpenAI


class BaseAgent:
    """
    Foundation class for all specialized agents.
    Each agent has a name, a system prompt that defines its persona,
    and a run() method that processes input and returns structured output.
    """

    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        self._client: OpenAI | None = None

    @property
    def client(self) -> OpenAI:
        if self._client is None:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise EnvironmentError(
                    "OPENAI_API_KEY environment variable is not set."
                )
            self._client = OpenAI(api_key=api_key)
        return self._client

    def run(self, input_text: str, context: str = "") -> str:
        """
        Process the input text and return a structured response.

        Args:
            input_text: The main query or content to analyze.
            context: Optional context from memory or other agents.

        Returns:
            Structured string output from this agent.
        """
        messages = [{"role": "system", "content": self.system_prompt}]

        if context:
            messages.append(
                {
                    "role": "user",
                    "content": f"Previous context:\n{context}\n\nCurrent input:\n{input_text}",
                }
            )
        else:
            messages.append({"role": "user", "content": input_text})

        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
        )

        return response.choices[0].message.content.strip()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} name='{self.name}'>"
