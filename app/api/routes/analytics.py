from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.dependencies.database import get_db
from app.services.analytics_service import get_dashboard_kpis

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/kpis")
def read_kpis(db: Session = Depends(get_db)):
    return get_dashboard_kpis(db)