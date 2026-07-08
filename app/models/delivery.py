from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums import DeliveryStatus


class Delivery(BaseModel, Base):
    __tablename__ = "deliveries"

    cte_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    invoice_number: Mapped[str] = mapped_column(String(30), nullable=False)

    origin_city: Mapped[str] = mapped_column(String(80), nullable=False)
    origin_state: Mapped[str] = mapped_column(String(2), nullable=False)

    weight_tons: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    freight_value: Mapped[Decimal] = mapped_column(Numeric(12, 2), nullable=False)
    distance_km: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    planned_departure_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estimated_delivery_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    actual_departure_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    actual_delivery_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[DeliveryStatus] = mapped_column(
        Enum(DeliveryStatus, name="delivery_status"),
        nullable=False,
        default=DeliveryStatus.CREATED,
    )

    carrier_id: Mapped[UUID] = mapped_column(ForeignKey("carriers.id"), nullable=False)
    driver_id: Mapped[UUID] = mapped_column(ForeignKey("drivers.id"), nullable=False)
    truck_id: Mapped[UUID] = mapped_column(ForeignKey("trucks.id"), nullable=False)
    customer_id: Mapped[UUID] = mapped_column(ForeignKey("customers.id"), nullable=False)
    route_id: Mapped[UUID] = mapped_column(ForeignKey("routes.id"), nullable=False)


    carrier = relationship("Carrier", back_populates="deliveries")
    driver = relationship("Driver", back_populates="deliveries")
    truck = relationship("Truck", back_populates="deliveries")
    customer = relationship("Customer", back_populates="deliveries")


    events = relationship("DeliveryEvent", back_populates="delivery")
    occurrences = relationship("Occurrence", back_populates="delivery")

    route = relationship("Route", back_populates="deliveries")

    