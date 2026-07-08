from datetime import datetime, timedelta
from decimal import Decimal

from sqlalchemy.orm import Session

from app.models.delivery import Delivery
from app.models.enums import DeliveryStatus, LogisticsEventType, TruckStatus, DriverStatus
from app.models.truck import Truck
from app.models.driver import Driver
from app.seed.static_data import ORIGIN
from app.simulator.event_engine import register_delivery_event


def evolve_deliveries(db: Session, now: datetime) -> int:
    deliveries = (
        db.query(Delivery)
        .filter(
            Delivery.status.in_(
                [
                    DeliveryStatus.WAITING_LOADING,
                    DeliveryStatus.LOADING,
                    DeliveryStatus.LOADED,
                    DeliveryStatus.IN_TRANSIT,
                    DeliveryStatus.WAITING_UNLOADING,
                    DeliveryStatus.UNLOADING,
                ]
            )
        )
        .all()
    )

    updated_count = 0

    for delivery in deliveries:
        updated = evolve_delivery(db, delivery, now)

        if updated:
            updated_count += 1

    db.commit()

    return updated_count


def evolve_delivery(db: Session, delivery: Delivery, now: datetime) -> bool:
    truck = db.query(Truck).filter(Truck.id == delivery.truck_id).first()
    driver = db.query(Driver).filter(Driver.id == delivery.driver_id).first()

    if not truck or not driver:
        return False

    if delivery.status == DeliveryStatus.WAITING_LOADING:
        if now >= delivery.planned_departure_at - timedelta(minutes=20):
            delivery.status = DeliveryStatus.LOADING
            truck.status = TruckStatus.LOADING

            register_delivery_event(
                db=db,
                delivery_id=delivery.id,
                event_type=LogisticsEventType.LOADING_STARTED,
                event_time=now,
                latitude=Decimal(str(ORIGIN["latitude"])),
                longitude=Decimal(str(ORIGIN["longitude"])),
                description="Carregamento iniciado.",
                responsible_area="Warehouse",
            )

            return True

    if delivery.status == DeliveryStatus.LOADING:
        delivery.status = DeliveryStatus.LOADED
        truck.status = TruckStatus.LOADED

        register_delivery_event(
            db=db,
            delivery_id=delivery.id,
            event_type=LogisticsEventType.LOADING_FINISHED,
            event_time=now,
            latitude=Decimal(str(ORIGIN["latitude"])),
            longitude=Decimal(str(ORIGIN["longitude"])),
            description="Carregamento finalizado.",
            responsible_area="Warehouse",
        )

        return True

    if delivery.status == DeliveryStatus.LOADED:
        if now >= delivery.planned_departure_at:
            delivery.status = DeliveryStatus.IN_TRANSIT
            delivery.actual_departure_at = now
            truck.status = TruckStatus.IN_TRANSIT
            truck.current_speed_kmh = int(delivery.route.average_speed_kmh)

            register_delivery_event(
                db=db,
                delivery_id=delivery.id,
                event_type=LogisticsEventType.DEPARTED_ORIGIN,
                event_time=now,
                latitude=Decimal(str(ORIGIN["latitude"])),
                longitude=Decimal(str(ORIGIN["longitude"])),
                description="Caminhão saiu da origem.",
                responsible_area="Transport",
            )

            return True

    if delivery.status == DeliveryStatus.IN_TRANSIT:
        if now >= delivery.estimated_delivery_at:
            delivery.status = DeliveryStatus.WAITING_UNLOADING
            truck.status = TruckStatus.WAITING_UNLOADING
            truck.current_speed_kmh = 0
            truck.current_latitude = delivery.route.destination_latitude
            truck.current_longitude = delivery.route.destination_longitude

            register_delivery_event(
                db=db,
                delivery_id=delivery.id,
                event_type=LogisticsEventType.ARRIVED_CUSTOMER,
                event_time=now,
                latitude=delivery.route.destination_latitude,
                longitude=delivery.route.destination_longitude,
                description="Caminhão chegou ao cliente.",
                responsible_area="Transport",
            )

            return True

    if delivery.status == DeliveryStatus.WAITING_UNLOADING:
        delivery.status = DeliveryStatus.UNLOADING
        truck.status = TruckStatus.UNLOADING

        register_delivery_event(
            db=db,
            delivery_id=delivery.id,
            event_type=LogisticsEventType.UNLOADING_STARTED,
            event_time=now,
            latitude=delivery.route.destination_latitude,
            longitude=delivery.route.destination_longitude,
            description="Descarga iniciada.",
            responsible_area="Customer",
        )

        return True

    if delivery.status == DeliveryStatus.UNLOADING:
        delivery.status = DeliveryStatus.DELIVERED
        delivery.actual_delivery_at = now

        truck.status = TruckStatus.AVAILABLE
        truck.current_speed_kmh = 0

        driver.status = DriverStatus.AVAILABLE

        register_delivery_event(
            db=db,
            delivery_id=delivery.id,
            event_type=LogisticsEventType.DELIVERY_COMPLETED,
            event_time=now,
            latitude=delivery.route.destination_latitude,
            longitude=delivery.route.destination_longitude,
            description="Entrega concluída.",
            responsible_area="Customer",
        )

        return True

    return False