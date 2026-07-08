from datetime import UTC, datetime, timedelta

import app.db.models

from app.core.settings import settings
from app.db.session import SessionLocal
from app.simulator.delivery_engine import create_delivery

class SimulationEngine:
    def __init__(self) -> None:
        self.current_time = datetime.now(UTC)

    def tick(self) -> None:
        self.current_time += timedelta(seconds=settings.SIMULATION_SPEED_SECONDS)

        db = SessionLocal()

        try:
            delivery = create_delivery(db, now=self.current_time)

            if delivery:
                print(f"Nova entrega criada: {delivery.cte_number}")

        finally:
            db.close()


if __name__ == "__main__":
    engine = SimulationEngine()

    while True:
        engine.tick()