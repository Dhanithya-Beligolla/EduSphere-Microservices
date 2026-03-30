"""
Log-based event publisher — writes events to structured logs.
Useful for development and debugging.
"""

from app.events.base import DomainEvent, EventPublisher
from app.core.logging import get_logger

logger = get_logger("events.publisher")


class LogPublisher(EventPublisher):
    """Publishes events by writing them to structured logs."""

    async def publish(self, event: DomainEvent) -> None:
        logger.info(
            "domain_event_published",
            event_type=event.event_type,
            event_id=event.event_id,
            aggregate_id=event.aggregate_id,
            payload=event.payload,
            timestamp=event.timestamp,
        )

    async def publish_many(self, events: list[DomainEvent]) -> None:
        for event in events:
            await self.publish(event)
