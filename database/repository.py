from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.models import Base, CustomerRecord

# -------------------------------
# Database Configuration
# -------------------------------

DATABASE_URL = "sqlite:///database.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create tables if they do not exist
Base.metadata.create_all(engine)

SessionLocal = sessionmaker(bind=engine)


# -------------------------------
# Save Records Function
# -------------------------------

def save_records(df):
    """
    Saves processed customer records into the SQLite database.
    """

    session = SessionLocal()

    try:
        for _, row in df.iterrows():

            record = CustomerRecord(
                revenue=float(row["revenue"]),
                frequency=int(row["frequency"]),
                segment=str(row["segment"]),
                revenue_per_transaction=float(
                    row.get("revenue_per_transaction", 0)
                )
            )

            session.add(record)

        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()