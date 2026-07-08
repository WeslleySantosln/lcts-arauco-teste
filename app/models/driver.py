from sqlalchemy import Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base import BaseModel
from app.models.enums import DriverStatus


class Driver(BaseModel, Base):
    __tablename__ = "drivers"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    license_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    experience_years: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    status: Mapped[DriverStatus] = mapped_column(
        Enum(DriverStatus, name="driver_status"),
        nullable=False,
        default=DriverStatus.AVAILABLE,
    )

    carrier_id = mapped_column(ForeignKey("carriers.id"), nullable=False)

    carrier = relationship("Carrier", back_populates="drivers")
    trucks = relationship("Truck", back_populates="driver")
    deliveries = relationship("Delivery", back_populates="driver")