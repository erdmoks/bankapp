from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from controllers.auth_controller import login_required
from models.customer import get_customer_by_id, make_transfer
from database import get_db
import html

transfer_bp = Blueprint("transfer", __name__)

@transfer_bp.route("/transfer", methods=["POST"])
@login_required
def transfer_money():
    sender_id = html.escape(session.get("customer_id").strip())
    receiver_id = html.escape(request.form.get("receiver_id").strip())
    amount_raw = html.escape(request.form.get("amount").strip())
    description = html.escape(request.form.get("description", "").strip())

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
    
    receiver = get_customer_by_id(receiver_id)
    if not receiver:
        raise ValueError("Alıcı müşteri bulunamadı.")
    
    sender = get_customer_by_id(sender_id)
    if sender["balance"] < amount:
        raise ValueError("Yetersiz bakiye.")

    try: 
        make_transfer(sender_id, receiver_id, amount, description)
        flash("Transfer işlemi başarıyla tamamlandı.", "success")
    except Exception as e:
        flash("Transfer işlemi sırasında bir hata oluştu.", "error")
    return redirect(url_for("transfer.transfer_page"))

@transfer_bp.route("/transfer", methods=["GET"])
@login_required
def transfer_page(customer):
    '''customer_id = session.get("customer_id")
    if not customer_id:
        flash("Devam etmek için giriş yapın.", "error")
        return redirect(url_for("auth.login"))
    '''
    db = get_db()

    transactions = db.execute(
        """
        SELECT * FROM transactions
        WHERE sender_customer_id = ? OR receiver_customer_id = ?
        ORDER BY created_at DESC
        """,
        (customer["customer_id"], customer["customer_id"])
    ).fetchall()

    return render_template("transfer.html", customer=customer, transactions=transactions)