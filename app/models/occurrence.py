from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums import OccurrenceSeverity, OccurrenceType


class Occurrence(BaseModel, Base):
    __tablename__ = "occurrences"

    delivery_id: Mapped[UUID] = mapped_column(
        ForeignKey("deliveries.id"),
        nullable=False,
        index=True,
    )

    occurrence_type: Mapped[OccurrenceType] = mapped_column(
        Enum(OccurrenceType, name="occurrence_type"),
        nullable=False,
        index=True,
    )

    severity: Mapped[OccurrenceSeverity] = mapped_column(
        Enum(OccurrenceSeverity, name="occurrence_severity"),
        nullable=False,
    )

    occurred_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    delay_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    latitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 6), nullable=True)
    longitude: Mapped[Decimal | None] = mapped_column(Numeric(10, 6), nullable=True)

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    delivery = relationship("Delivery", back_populates="occurrences")