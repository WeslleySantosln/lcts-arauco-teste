from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy.orm import Session

from app.models.delivery_event import DeliveryEvent
from app.models.enums import LogisticsEventType


def register_delivery_event(
    db: Session,
    delivery_id: UUID,
    event_type: LogisticsEventType,
    event_time: datetime,
    latitude: Decimal | None = None,
    longitude: Decimal | None = None,
    description: str | None = None,
    responsible_area: str | None = None,
) -> DeliveryEvent:
    event = DeliveryEvent(
        delivery_id=delivery_id,
        event_type=event_type,
        event_time=event_time,
        latitude=latitude,
        longitude=longitude,
        description=description,
        responsible_area=responsible_area,
    )

    db.add(event)

    return event