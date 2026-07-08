from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel


class TruckPosition(BaseModel, Base):
    __tablename__ = "truck_positions"

    truck_id: Mapped[UUID] = mapped_column(ForeignKey("trucks.id"), nullable=False, index=True)
    delivery_id: Mapped[UUID] = mapped_column(ForeignKey("deliveries.id"), nullable=False, index=True)

    latitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)
    longitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)

    speed_kmh: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    progress_percent: Mapped[Decimal] = mapped_column(Numeric(5, 2), nullable=False, default=0)

    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)

    truck = relationship("Truck", back_populates="positions")
    delivery = relationship("Delivery", back_populates="positions")