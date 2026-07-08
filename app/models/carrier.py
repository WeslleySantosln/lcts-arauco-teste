from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.models.base import BaseModel


class Carrier(BaseModel, Base):
    __tablename__ = "carriers"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    document: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    city: Mapped[str] = mapped_column(String(80), nullable=False)
    state: Mapped[str] = mapped_column(String(2), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)