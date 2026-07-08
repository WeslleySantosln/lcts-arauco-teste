from datetime import UTC, datetime, timedelta
from decimal import Decimal
from random import choice, randint

from sqlalchemy.orm import Session

from app.core.settings import settings
from app.models.carrier import Carrier
from app.models.customer import Customer
from app.models.delivery import Delivery
from app.models.driver import Driver
from app.models.enums import DeliveryStatus, DriverStatus, LogisticsEventType, TruckStatus
from app.models.route import Route
from app.models.truck import Truck
from app.seed.static_data import ORIGIN
from app.simulator.event_engine import register_delivery_event


def count_active_deliveries(db: Session) -> int:
    return (
        db.query(Delivery)
        .filter(
            Delivery.status.in_(
                [
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
            )
        )
        .count()
    )


def get_available_truck(db: Session) -> Truck | None:
    return (
        db.query(Truck)
        .filter(Truck.status == TruckStatus.AVAILABLE)
        .order_by(Truck.created_at.asc())
        .first()
    )


def get_available_driver(db: Session, carrier_id) -> Driver | None:
    return (
        db.query(Driver)
        .filter(
            Driver.carrier_id == carrier_id,
            Driver.status == DriverStatus.AVAILABLE,
        )
        .order_by(Driver.created_at.asc())
        .first()
    )


def create_delivery(db: Session, now: datetime | None = None) -> Delivery | None:
    now = now or datetime.now(UTC)

    if count_active_deliveries(db) >= settings.MAX_ACTIVE_DELIVERIES:
        return None

    truck = get_available_truck(db)

    if not truck:
        return None

    driver = get_available_driver(db, truck.carrier_id)

    if not driver:
        return None

    route = choice(db.query(Route).all())
    customer = (
        db.query(Customer)
        .filter(
            Customer.city == route.destination_city,
            Customer.state == route.destination_state,
        )
        .first()
    )

    carrier = db.query(Carrier).filter(Carrier.id == truck.carrier_id).first()

    if not customer or not carrier:
        return None

    planned_departure_at = now + timedelta(minutes=randint(10, 40))
    estimated_delivery_at = planned_departure_at + timedelta(
        hours=route.estimated_duration_hours
    )

    delivery = Delivery(
        cte_number=f"CTE-{randint(100000, 999999)}",
        invoice_number=f"NF-{randint(100000, 999999)}",
        origin_city=ORIGIN["city"],
        origin_state=ORIGIN["state"],
        weight_tons=Decimal(str(randint(20, 45))),
        freight_value=Decimal(str(randint(6_000, 28_000))),
        distance_km=route.distance_km,
        planned_departure_at=planned_departure_at,
        estimated_delivery_at=estimated_delivery_at,
        status=DeliveryStatus.WAITING_LOADING,
        carrier_id=carrier.id,
        driver_id=driver.id,
        truck_id=truck.id,
        customer_id=customer.id,
        route_id=route.id,
    )

    db.add(delivery)
    db.flush()

    truck.status = TruckStatus.WAITING_LOADING
    truck.driver_id = driver.id
    driver.status = DriverStatus.ON_TRIP

    register_delivery_event(
        db=db,
        delivery_id=delivery.id,
        event_type=LogisticsEventType.DELIVERY_CREATED,
        event_time=now,
        latitude=Decimal(str(ORIGIN["latitude"])),
        longitude=Decimal(str(ORIGIN["longitude"])),
        description="CT-e criado automaticamente pelo simulador.",
        responsible_area="Control Tower",
    )

    register_delivery_event(
        db=db,
        delivery_id=delivery.id,
        event_type=LogisticsEventType.DELIVERY_PLANNED,
        event_time=now,
        latitude=Decimal(str(ORIGIN["latitude"])),
        longitude=Decimal(str(ORIGIN["longitude"])),
        description="Entrega planejada e recursos alocados.",
        responsible_area="Planning",
    )

    db.commit()

    return delivery