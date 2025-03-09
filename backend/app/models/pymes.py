# models/pymes.py
import enum
from sqlalchemy import Column, Integer, String, SmallInteger, Enum
from app.models.base import Base

class TierEnum(enum.Enum):
    NA = "N/A"
    PLATA = "Plata"
    ORO = "Oro"
    PLATINO = "Platino"

class PymeTrust(Base):
    __tablename__ = "pymes_trust"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(13), unique=True, nullable=False)
    pyme_name = Column(String(35), nullable=False)
    trust_score = Column(SmallInteger, nullable=False)
    # Force SQLAlchemy to use the enum's values (i.e. "Plata", "Oro", etc.)
    tier = Column(
        Enum(TierEnum, values_callable=lambda enum_cls: [e.value for e in enum_cls]),
        nullable=False,
        default=TierEnum.NA
    )

class MockLogIn(Base):
    __tablename__ = "mock_log_in"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(13), unique=True, nullable=False)
    password = Column(String(16), nullable=False)
