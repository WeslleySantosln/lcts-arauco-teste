from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel


class Route(BaseModel, Base):
    __tablename__ = "routes"

    origin_city: Mapped[str] = mapped_column(String(80), nullable=False)
    origin_state: Mapped[str] = mapped_column(String(2), nullable=False)

    origin_latitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)
    origin_longitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)

    destination_city: Mapped[str] = mapped_column(String(80), nullable=False)
    destination_state: Mapped[str] = mapped_column(String(2), nullable=False)

    destination_latitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)
    destination_longitude: Mapped[Decimal] = mapped_column(Numeric(10, 6), nullable=False)

    distance_km: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    estimated_duration_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    average_speed_kmh: Mapped[int] = mapped_column(Integer, nullable=False, default=60)

    deliveries = relationship("Delivery", back_populates="route")