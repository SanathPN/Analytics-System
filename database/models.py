from sqlalchemy import create_engine, Column, Integer, Float, String
from sqlalchemy.orm import declarative_base

# Base class for models
Base = declarative_base()

# SQLite database connection
engine = create_engine("sqlite:///database.db", echo=False)


class Customer(Base):
    """
    Customer Table Structure
    Stores processed analytics records
    """

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, autoincrement=True)
    revenue = Column(Float, nullable=False)
    frequency = Column(Integer, nullable=False)
    segment = Column(String(50), nullable=False)
    revenue_per_transaction = Column(Float, nullable=True)
    normalized_revenue = Column(Float, nullable=True)


# Create tables in database (if not already created)
def init_db():
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    init_db()
    print("Database and tables created successfully.")