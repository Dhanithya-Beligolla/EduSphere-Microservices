"""
Domain event base classes and publisher abstraction.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any
import uuid


@dataclass
class DomainEvent:
    """Base class for all domain events."""
    event_type: str
    aggregate_id: str
    payload: dict[str, Any] = field(default_factory=dict)
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    source: str = "learning-materials-service"


class EventPublisher(ABC):
    """
    Abstract event publisher interface.
    Implement for Kafka, RabbitMQ, NATS, or any message bus.
    """

    @abstractmethod
    async def publish(self, event: DomainEvent) -> None:
        """Publish a single domain event."""
        ...

    @abstractmethod
    async def publish_many(self, events: list[DomainEvent]) -> None:
        """Publish multiple domain events."""
        ...
