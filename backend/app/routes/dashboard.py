# app/routes/dashboard.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models.base import PymeTrust

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/")
def get_dashboard(ruc: str, db: Session = Depends(get_db)):
    """
    Returns summary data for the user's dashboard:
      - Current trust level
      - Certifications completed
      - References
      - Activity log
      - Confidence evolution
    """
    pyme = db.query(PymeTrust).filter(PymeTrust.ruc == ruc).first()
    if not pyme:
        return {
            "nivelConfianza": 0,
            "certificaciones": {"completadas": 0, "totales": 0},
            "referencias": 0,
            "actividadReciente": [],
            "graficoEvolucion": [],
        }

    return {
        "nivelConfianza": pyme.trust_score,  # e.g. 75
        "certificaciones": {"completadas": 3, "totales": 5},  # mocked
        "referencias": 12,  # mocked
        "actividadReciente": [
            "Distribuidora Nacional S.A. te calificó",
            "Certificación Fiscal completada",
            "Financiera Progreso te otorgó un crédito",
        ],
        "graficoEvolucion": [60, 68, 75],  # mocked historical scores
    }
