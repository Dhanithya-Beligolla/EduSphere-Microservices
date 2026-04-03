"""
group_core/events.py
Async event publisher.
Publishes domain events:
  - group.group.created
  - group.activity.published
  - group.submission.created
  - group.peer-evaluation.submitted
  - group.result.published

In an MVP, events are logged. In production, replace with Kafka/RabbitMQ/Redis Pub-Sub.
"""

import logging
from datetime import datetime, timezone
from enum import Enum
import uuid

logger = logging.getLogger(__name__)


class GroupEvent(str, Enum):
    GROUP_CREATED = "group.group.created"
    ACTIVITY_PUBLISHED = "group.activity.published"
    SUBMISSION_CREATED = "group.submission.created"
    PEER_EVAL_SUBMITTED = "group.peer-evaluation.submitted"
    RESULT_PUBLISHED = "group.result.published"


async def publish_event(event_type: GroupEvent, payload: dict):
    """
    Publish a domain event.
    MVP: logs the event. Replace body with message broker call in production.
    """
    event = {
        "eventId": str(uuid.uuid4()),
        "eventType": event_type.value,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "payload": payload,
    }
    logger.info(f"[EVENT PUBLISHED] {event_type.value}: {event}")
    # TODO: await kafka_producer.send(event_type.value, event)
    return event
