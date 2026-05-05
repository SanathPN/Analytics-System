from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class CustomerRecord(Base):
    __tablename__ = "customer_records"

    id = Column(Integer, primary_key=True, index=True)
    revenue = Column(Float, nullable=False)
    frequency = Column(Integer, nullable=False)
    segment = Column(String, nullable=False)
    revenue_per_transaction = Column(Float)