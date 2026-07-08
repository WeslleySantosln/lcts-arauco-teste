from decimal import Decimal
from uuid import UUID

from sqlalchemy import Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums import TruckStatus


class Truck(BaseModel, Base):
    __tablename__ = "trucks"

    plate: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)
    model: Mapped[str] = mapped_column(String(80), nullable=False)

    capacity_tons: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    current_latitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 6),
        nullable=False,
    )

    current_longitude: Mapped[Decimal] = mapped_column(
        Numeric(10, 6),
        nullable=False,
    )

    current_speed_kmh: Mapped[int] = mapped_column(nullable=False, default=0)

    status: Mapped[TruckStatus] = mapped_column(
        Enum(TruckStatus, name="truck_status"),
        nullable=False,
        default=TruckStatus.AVAILABLE,
    )

    carrier_id: Mapped[UUID] = mapped_column(ForeignKey("carriers.id"), nullable=False)
    driver_id: Mapped[UUID | None] = mapped_column(ForeignKey("drivers.id"), nullable=True)

    carrier = relationship("Carrier", back_populates="trucks")
    driver = relationship("Driver", back_populates="trucks")
    deliveries = relationship("Delivery", back_populates="truck")