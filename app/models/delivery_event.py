from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums import LogisticsEventType


class DeliveryEvent(BaseModel, Base):
    __tablename__ = "delivery_events"

    delivery_id: Mapped[UUID] = mapped_column(
        ForeignKey("deliveries.id"),
        nullable=False,
        index=True,
    )

    event_type: Mapped[LogisticsEventType] = mapped_column(
        Enum(LogisticsEventType, name="logistics_event_type"),
        nullable=False,
        index=True,
    )

    event_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 6),
        nullable=True,
    )

    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    responsible_area: Mapped[str | None] = mapped_column(String(80), nullable=True)

    delivery = relationship("Delivery", back_populates="events")