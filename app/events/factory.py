"""
Event publisher factory.
Returns the correct publisher implementation based on config.
"""

from app.core.config import settings
from app.events.base import EventPublisher
from app.events.publishers.noop import NoopPublisher
from app.events.publishers.log_publisher import LogPublisher


def get_event_publisher() -> EventPublisher:
    """
    Factory function returning the configured event publisher.
    Reads EVENT_PUBLISHER from settings (default: 'noop').
    """
    publisher_type = settings.event_publisher.lower()

    if publisher_type == "log":
        return LogPublisher()
    else:
        return NoopPublisher()
