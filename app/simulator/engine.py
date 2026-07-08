from datetime import UTC, datetime, timedelta
from time import sleep

import app.db.models

from app.core.settings import settings
from app.db.session import SessionLocal
from app.simulator.delivery_engine import create_delivery
from app.simulator.status_engine import evolve_deliveries
from app.simulator.gps_engine import update_gps_positions


class SimulationEngine:
    def __init__(self) -> None:
        self.current_time = datetime.now(UTC)

    def tick(self) -> None:
        self.current_time += timedelta(seconds=settings.SIMULATION_SPEED_SECONDS)

        db = SessionLocal()

        try:
            delivery = create_delivery(db, now=self.current_time)
            updated_count = evolve_deliveries(db, now=self.current_time)
            gps_updates = update_gps_positions(db, now=self.current_time)

            if delivery:
                print(f"Nova entrega criada: {delivery.cte_number}")

            if updated_count:
                print(f"Entregas atualizadas: {updated_count}")
                
            if gps_updates:
                print(f"Posições GPS atualizadas: {gps_updates}")

        finally:
            db.close()


if __name__ == "__main__":
    engine = SimulationEngine()

    while True:
        engine.tick()
        sleep(settings.SIMULATION_INTERVAL_SECONDS)