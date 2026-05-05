from sqlalchemy.orm import sessionmaker
from database.models import engine, Customer


# Create session factory
Session = sessionmaker(bind=engine)


def save_to_database(df):
    """
    Saves processed dataframe records into the database.
    Clears previous data for fresh demo runs.
    """

    session = Session()

    try:
        # Optional: Clear existing records (useful for demo reset)
        session.query(Customer).delete()

        for _, row in df.iterrows():
            customer = Customer(
                revenue=float(row["revenue"]),
                frequency=int(row["frequency"]),
                segment=row["segment"],
                revenue_per_transaction=float(
                    row.get("revenue_per_transaction", 0)
                ),
                normalized_revenue=float(
                    row.get("normalized_revenue", 0)
                )
            )

            session.add(customer)

        session.commit()

    except Exception as e:
        session.rollback()
        raise e

    finally:
        session.close()


def fetch_all_records():
    """
    Fetch all records from database.
    Useful for dashboard extension.
    """
    session = Session()
    records = session.query(Customer).all()
    session.close()
    return records


def fetch_segment_summary():
    """
    Returns revenue summary grouped by segment.
    """
    session = Session()

    results = (
        session.query(
            Customer.segment,
            Customer.revenue
        )
        .all()
    )

    session.close()

    summary = {}
    for segment, revenue in results:
        summary[segment] = summary.get(segment, 0) + revenue

    return summary