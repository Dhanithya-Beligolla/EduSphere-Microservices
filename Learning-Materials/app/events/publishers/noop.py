"""
No-op event publisher — discards all events silently.
Default publisher when no message bus is configured.
"""

from app.events.base import DomainEvent, EventPublisher


class NoopPublisher(EventPublisher):
    """Discards all events. Used when eventing is not needed."""

    async def publish(self, event: DomainEvent) -> None:
        pass

    async def publish_many(self, events: list[DomainEvent]) -> None:
        pass
