# models/pymes.py
import enum
from sqlalchemy import Column, Integer, String, SmallInteger, Enum, Boolean, UniqueConstraint, DateTime, func, Float, Date
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

class PymeCertifications(Base):
    __tablename__ = "pymes_certificates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(13), nullable=False)
    certificate_name = Column(String(250), nullable=False)
    issuer = Column(String(250), nullable=False)
    issue_date = Column(Date, nullable=True)
    expiration_date = Column(Date, nullable=True)


class PeerPymesTrustScore(Base):
    __tablename__ = "peer_pymes_trust_scores"
    id = Column(Integer, primary_key=True, autoincrement=True)
    score_issuer = Column(String(13), nullable=False)
    score_receiver = Column(String(13), nullable=False)
    peer_trust_score = Column(SmallInteger, nullable=False, default=0)

class PymeConnection(Base):
    __tablename__ = "pyme_connections"
    id = Column(Integer, primary_key=True, autoincrement=True)
    requester_ruc = Column(String(13), nullable=False)
    receiver_ruc = Column(String(13), nullable=False)
    status = Column(
        Enum("Pending", "Accepted", "Rejected", name="connection_status"),
        nullable=False,
        default="Pending"
    )
    requested_at = Column(DateTime, server_default=func.now())
    accepted_at = Column(DateTime, nullable=True)
    # Avoid duplicate requests
    __table_args__ = (
        UniqueConstraint("requester_ruc", "receiver_ruc", name="unique_connection"),
    )

class CreditOption(Base):
    __tablename__ = "credit_options"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    amount = Column(String(50), nullable=False)
    interest_rate = Column(String(20), nullable=False)
    term = Column(String(50), nullable=False)
    requirements = Column(String(100), nullable=False)
    recommended = Column(Boolean, default=False)
    link = Column(String(255), nullable=False)

class PymeCredit(Base):
    __tablename__ = "pyme_credits"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(13), nullable=False)
    credit_type_id = Column(Integer, nullable=False)
    amount_approved = Column(Integer, nullable=False)
    interest_rate = Column(Float, nullable=False)
    term = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    progress_percentage = Column(SmallInteger, default=0)
    status = Column(
        Enum("Active", "Completed", "Cancelled", name="credit_status"),
        default="Active"
    )