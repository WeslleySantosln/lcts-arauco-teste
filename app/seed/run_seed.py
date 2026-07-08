from decimal import Decimal
from random import choice, randint
from uuid import uuid4

from faker import Faker
from sqlalchemy.orm import Session

import app.db.models
from app.models.route import Route

from app.db.session import SessionLocal
from app.models.carrier import Carrier
from app.models.customer import Customer
from app.models.driver import Driver
from app.models.enums import DriverStatus, TruckStatus
from app.models.truck import Truck
from app.seed.static_data import CARRIERS, CUSTOMERS, ORIGIN, TRUCK_MODELS

fake = Faker("pt_BR")

def create_routes(db: Session, customers: list[Customer]) -> list[Route]:
    routes: list[Route] = []

    for customer in customers:
        existing = (
            db.query(Route)
            .filter(
                Route.origin_city == ORIGIN["city"],
                Route.origin_state == ORIGIN["state"],
                Route.destination_city == customer.city,
                Route.destination_state == customer.state,
            )
            .first()
        )

        if existing:
            routes.append(existing)
            continue

        distance_km = Decimal(str(randint(250, 1200)))
        average_speed_kmh = randint(55, 75)
        estimated_duration_hours = max(1, int(distance_km / average_speed_kmh))

        route = Route(
            origin_city=ORIGIN["city"],
            origin_state=ORIGIN["state"],
            origin_latitude=Decimal(str(ORIGIN["latitude"])),
            origin_longitude=Decimal(str(ORIGIN["longitude"])),
            destination_city=customer.city,
            destination_state=customer.state,
            destination_latitude=customer.latitude,
            destination_longitude=customer.longitude,
            distance_km=distance_km,
            estimated_duration_hours=estimated_duration_hours,
            average_speed_kmh=average_speed_kmh,
        )

        db.add(route)
        routes.append(route)

    db.commit()

    return routes


def create_carriers(db: Session) -> list[Carrier]:
    carriers: list[Carrier] = []

    for item in CARRIERS:
        existing = db.query(Carrier).filter(Carrier.document == item["document"]).first()

        if existing:
            carriers.append(existing)
            continue

        carrier = Carrier(**item)
        db.add(carrier)
        carriers.append(carrier)

    db.commit()

    return carriers


def create_customers(db: Session) -> list[Customer]:
    customers: list[Customer] = []

    for item in CUSTOMERS:
        existing = db.query(Customer).filter(Customer.document == item["document"]).first()

        if existing:
            customers.append(existing)
            continue

        customer = Customer(
            name=item["name"],
            document=item["document"],
            city=item["city"],
            state=item["state"],
            latitude=Decimal(str(item["latitude"])),
            longitude=Decimal(str(item["longitude"])),
        )

        db.add(customer)
        customers.append(customer)

    db.commit()

    return customers


def create_drivers(db: Session, carriers: list[Carrier], quantity: int = 75) -> list[Driver]:
    drivers: list[Driver] = []

    current_count = db.query(Driver).count()

    if current_count >= quantity:
        return db.query(Driver).all()

    for index in range(quantity - current_count):
        carrier = choice(carriers)

        driver = Driver(
            name=fake.name(),
            license_number=f"CNH-{uuid4().hex[:10].upper()}",
            phone=fake.phone_number(),
            experience_years=randint(1, 25),
            status=DriverStatus.AVAILABLE,
            carrier_id=carrier.id,
        )

        db.add(driver)
        drivers.append(driver)

    db.commit()

    return db.query(Driver).all()


def create_trucks(db: Session, carriers: list[Carrier], drivers: list[Driver], quantity: int = 60) -> list[Truck]:
    current_count = db.query(Truck).count()

    if current_count >= quantity:
        return db.query(Truck).all()

    available_drivers = drivers.copy()

    for index in range(quantity - current_count):
        carrier = choice(carriers)
        driver = available_drivers.pop() if available_drivers else None

        truck = Truck(
            plate=f"LCT{index:04d}",
            model=choice(TRUCK_MODELS),
            capacity_tons=Decimal(str(choice([35, 40, 45, 50]))),
            current_latitude=Decimal(str(ORIGIN["latitude"])),
            current_longitude=Decimal(str(ORIGIN["longitude"])),
            current_speed_kmh=0,
            odometer_km=Decimal(str(randint(50_000, 900_000))),
            last_maintenance_at=None,
            status=TruckStatus.AVAILABLE,
            carrier_id=carrier.id,
            driver_id=driver.id if driver else None,
        )

        db.add(truck)

    db.commit()

    return db.query(Truck).all()


def run_seed() -> None:
    db = SessionLocal()

    try:
        carriers = create_carriers(db)
        customers = create_customers(db)
        routes = create_routes(db, customers)
        drivers = create_drivers(db, carriers)
        trucks = create_trucks(db, carriers, drivers)

        print("Seed finalizado com sucesso.")
        print(f"Transportadoras: {len(carriers)}")
        print(f"Clientes: {len(customers)}")
        print(f"Motoristas: {len(drivers)}")
        print(f"Caminhões: {len(trucks)}")
        print(f"Rotas: {len(routes)}")

    finally:
        db.close()


if __name__ == "__main__":
    run_seed()