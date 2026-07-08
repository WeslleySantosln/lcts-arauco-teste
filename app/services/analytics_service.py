from datetime import UTC, datetime, time

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.models.enums import DeliveryStatus, TruckStatus
from app.models.truck import Truck


def get_dashboard_kpis(db: Session) -> dict:
    today_start = datetime.combine(
        datetime.now(UTC).date(),
        time.min,
        tzinfo=UTC,
    )

    active_statuses = [
        DeliveryStatus.CREATED,
        DeliveryStatus.PLANNED,
        DeliveryStatus.WAITING_LOADING,
        DeliveryStatus.LOADING,
        DeliveryStatus.LOADED,
        DeliveryStatus.IN_TRANSIT,
        DeliveryStatus.WAITING_UNLOADING,
        DeliveryStatus.UNLOADING,
        DeliveryStatus.DELAYED,
    ]

    active_deliveries = (
        db.query(func.count(Delivery.id))
        .filter(Delivery.status.in_(active_statuses))
        .scalar()
    )

    delivered_today = (
        db.query(func.count(Delivery.id))
        .filter(
            Delivery.status == DeliveryStatus.DELIVERED,
            Delivery.actual_delivery_at >= today_start,
        )
        .scalar()
    )

    delayed_deliveries = (
        db.query(func.count(Delivery.id))
        .filter(Delivery.status == DeliveryStatus.DELAYED)
        .scalar()
    )

    total_finished = (
        db.query(func.count(Delivery.id))
        .filter(
            Delivery.status == DeliveryStatus.DELIVERED,
            Delivery.actual_delivery_at.isnot(None),
        )
        .scalar()
    )

    on_time_finished = (
        db.query(func.count(Delivery.id))
        .filter(
            Delivery.status == DeliveryStatus.DELIVERED,
            Delivery.actual_delivery_at <= Delivery.estimated_delivery_at,
        )
        .scalar()
    )

    available_trucks = (
        db.query(func.count(Truck.id))
        .filter(Truck.status == TruckStatus.AVAILABLE)
        .scalar()
    )

    trucks_in_transit = (
        db.query(func.count(Truck.id))
        .filter(Truck.status == TruckStatus.IN_TRANSIT)
        .scalar()
    )

    otif_percent = 0

    if total_finished and total_finished > 0:
        otif_percent = round((on_time_finished / total_finished) * 100, 2)

    return {
        "active_deliveries": active_deliveries or 0,
        "delivered_today": delivered_today or 0,
        "delayed_deliveries": delayed_deliveries or 0,
        "available_trucks": available_trucks or 0,
        "trucks_in_transit": trucks_in_transit or 0,
        "otif_percent": otif_percent,
    }