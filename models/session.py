from database import get_db

def increment_session_version(customer_id):
    db = get_db()

    db.execute(
        """
        UPDATE customer
        SET session_version = session_version + 1
        WHERE customer_id = ?
        """,
        (customer_id,)
    )

    db.commit()

def increment_and_get_session_version(customer_id):
    db = get_db()
    db.execute(
        """
        UPDATE customer
        SET session_version = session_version + 1
        WHERE customer_id = ?
        """
        , (customer_id,)
    )

    db.commit()

    customer = db.execute(
        "SELECT session_version FROM customer WHERE customer_id = ?", (customer_id,)
    ).fetchone()
    return customer["session_version"] if customer else None

