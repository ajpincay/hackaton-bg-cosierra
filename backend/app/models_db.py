from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, SmallInteger

Base = declarative_base()

class PymeTrust(Base):
    __tablename__ = "pymes_trust"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(13), unique=True, nullable=False)
    pyme_name = Column(String(35), nullable=False)
    trust_score = Column(SmallInteger, nullable=False)
    tier = Column(SmallInteger, nullable=False)  # 0=Silver, 1=Gold, 2=Platinum

class MockLogIn(Base):
    __tablename__ = "mock_log_in"
    id = Column(Integer, primary_key=True, autoincrement=True)
    ruc = Column(String(50), unique=True, nullable=False)
    password = Column(String(16), nullable=False)
