 # SQLAlchemy models (DB table definitions)
# models.py

# SQLAlchemy models (DB table definitions)
from sqlalchemy import Column, Integer, String, Float, DateTime
from datetime import datetime
from .database import Base  # SQLAlchemy base class

# Defining a class that maps to a table called 'claims'
class Claim(Base):
    __tablename__ = "claims"  # Table name in the database

    id = Column(Integer, primary_key=True, index=True)  # Unique claim ID
    claimant_name = Column(String, nullable=False)  # Name of the claimant
    amount = Column(Float, nullable=False)  # Amount being claimed
    status = Column(String, default="submitted")  # Status of the claim
    submitted_at = Column(DateTime, default=datetime.utcnow)  # Timestamp of submission
    #claim_type = Column(String, nullable=False)
