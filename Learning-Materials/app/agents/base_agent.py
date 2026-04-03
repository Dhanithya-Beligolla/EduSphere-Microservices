"""
Base agent interface for internal automation modules.
All agents are deterministic — no LLM calls.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentResult:
    """Standard result from any agent execution."""
    success: bool
    data: dict[str, Any] = field(default_factory=dict)
    messages: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)


class BaseAgent(ABC):
    """Abstract base class for all agent modules."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name of the agent."""
        ...

    @abstractmethod
    async def execute(self, context: dict[str, Any]) -> AgentResult:
        """
        Execute the agent's task with the given context.

        Args:
            context: Dictionary containing input data for the agent.

        Returns:
            AgentResult with success/failure, data, and messages.
        """
        ...
