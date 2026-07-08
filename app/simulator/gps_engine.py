from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.models.enums import DeliveryStatus
from app.models.truck import Truck
from app.models.truck_position import TruckPosition


def update_gps_positions(db: Session, now: datetime) -> int:
    deliveries = (
        db.query(Delivery)
        .filter(Delivery.status == DeliveryStatus.IN_TRANSIT)
        .all()
    )

    updated_count = 0

    for delivery in deliveries:
        truck = db.query(Truck).filter(Truck.id == delivery.truck_id).first()

        if not truck or not delivery.actual_departure_at:
            continue

        total_seconds = (
            delivery.estimated_delivery_at - delivery.actual_departure_at
        ).total_seconds()

        elapsed_seconds = (now - delivery.actual_departure_at).total_seconds()

        if total_seconds <= 0:
            progress = Decimal("100")
        else:
            progress = Decimal(str(min(100, max(0, (elapsed_seconds / total_seconds) * 100))))

        origin_lat = Decimal(str(delivery.route.origin_latitude))
        origin_lon = Decimal(str(delivery.route.origin_longitude))
        dest_lat = Decimal(str(delivery.route.destination_latitude))
        dest_lon = Decimal(str(delivery.route.destination_longitude))

        factor = progress / Decimal("100")

        current_lat = origin_lat + ((dest_lat - origin_lat) * factor)
        current_lon = origin_lon + ((dest_lon - origin_lon) * factor)

        truck.current_latitude = current_lat
        truck.current_longitude = current_lon
        truck.current_speed_kmh = int(delivery.route.average_speed_kmh)

        position = TruckPosition(
            truck_id=truck.id,
            delivery_id=delivery.id,
            latitude=current_lat,
            longitude=current_lon,
            speed_kmh=truck.current_speed_kmh,
            progress_percent=progress.quantize(Decimal("0.01")),
            recorded_at=now,
        )

        db.add(position)
        updated_count += 1

    db.commit()

    return updated_count