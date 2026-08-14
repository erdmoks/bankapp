from database import get_db


def get_customer_by_email(email):
    return get_db().execute(
        "SELECT * FROM customer WHERE email = ?",
        (email,)
    ).fetchone()


def get_customer_by_id(customer_id):
    return get_db().execute(
        "SELECT * FROM customer WHERE customer_id = ?",
        (customer_id,)
    ).fetchone()


def update_customer_password(customer_id, password_hash):
    db = get_db()

    db.execute(
        """
        UPDATE customer
        SET password_hash = ?
        WHERE customer_id = ?
        """,
        (password_hash, customer_id)
    )

    db.commit()


def create_customer(
    customer_id,
    first_name,
    last_name,
    email,
    phone,
    birth_date,
    password_hash,
    created_at
):
    db = get_db()

    db.execute(
        """
        INSERT INTO customer
        (
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            birth_date,
            password_hash,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            customer_id,
            first_name,
            last_name,
            email,
            phone,
            birth_date,
            password_hash,
            created_at
        )
    )


    db.commit()

def make_transfer(sender_customer_id, receiver_customer_id, amount, description):
    db = get_db()

    receiver = get_customer_by_id(receiver_customer_id)
    if not receiver:
        raise ValueError("Alıcı müşteri bulunamadı.")

    sender = get_customer_by_id(sender_customer_id)
    if not sender:
        raise ValueError("Gönderen müşteri bulunamadı.")
    if sender["balance"] < amount:
        raise ValueError("Yetersiz bakiye.")

    db.execute(
        "UPDATE customer SET balance = balance - ? WHERE customer_id = ?",
        (amount, sender_customer_id)
    )
    db.execute(
        "UPDATE customer SET balance = balance + ? WHERE customer_id = ?",
        (amount, receiver_customer_id)
    )
    db.execute(
        """
        INSERT INTO transactions
        (sender_customer_id, receiver_customer_id, amount, description)
        VALUES (?, ?, ?, ?)
        """,
        (sender_customer_id, receiver_customer_id, amount, description)
    )
    db.commit()
