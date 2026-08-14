from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from models.customer import get_customer_by_id, make_transfer
from database import get_db
import html

transfer_bp = Blueprint("transfer", __name__)

@transfer_bp.route("/transfer", methods=["POST"])
def transfer_money():
    sender_id = html.escape(session.get("customer_id").strip())
    receiver_id = html.escape(request.form.get("receiver_id").strip())
    amount_raw = html.escape(request.form.get("amount").strip())
    description = html.escape(request.form.get("description", "").strip())

    if not receiver_id or not amount_raw:
        flash("Lütfen alıcı ve miktar bilgilerini girin.", "error")
        return redirect(url_for("transfer.transfer_page"))

    try:
        amount = int(amount_raw)
        if amount <= 0:
            flash("Transfer tutarı 0'dan büyük olmalıdır.", "error")
            return redirect(url_for("transfer.transfer_page"))
    except ValueError:
        flash("Geçerli bir transfer tutarı girin.", "error")
        return redirect(url_for("transfer.transfer_page"))
    if sender_id == receiver_id:
        flash("Kendinize para gönderemezsiniz.", "error")
        return redirect(url_for("transfer.transfer_page"))

    try: 
        make_transfer(sender_id, receiver_id, amount, description)
        flash("Transfer işlemi başarıyla tamamlandı.", "success")
    except ValueError as e:
        flash(str(e), "error")
    except Exception as e:
        flash("Transfer işlemi sırasında bir hata oluştu.", "error")
    return redirect(url_for("transfer.transfer_page"))

@transfer_bp.route("/transfer", methods=["GET"])
def transfer_page():
    customer_id = session.get("customer_id")
    if not customer_id:
        flash("Devam etmek için giriş yapın.", "error")
        return redirect(url_for("auth.login"))

    customer = get_customer_by_id(session.get("customer_id"))
    db = get_db()

    transactions = db.execute(
        """
        SELECT * FROM transactions
        WHERE sender_customer_id = ? OR receiver_customer_id = ?
        ORDER BY created_at DESC
        """,
        (customer_id, customer_id)
    ).fetchall()

    return render_template("transfer.html", customer=customer, transactions=transactions)