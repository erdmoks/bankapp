import html

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models.customer import (
    get_customer_by_id,
    update_customer_password
)

settings_bp = Blueprint("settings", __name__)

@settings_bp.route("/settings", methods=["GET", "POST"])
def change_password():
    customer_id = session.get("customer_id")

    if not customer_id:
        return redirect(url_for("auth.login"))

    customer = get_customer_by_id(customer_id)

    if customer is None:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        current_password = html.escape(request.form.get(
            "current_password",
            ""
        ))

        new_password = html.escape(request.form.get(
            "new_password",
            ""
        ))

        new_password_repeat = html.escape(request.form.get(
            "new_password_repeat",
            ""
        ))

        if not check_password_hash(
            customer["password_hash"],
            current_password
        ):
            flash(
                "Mevcut şifreniz doğru değil.",
                "error"
            )

        elif len(new_password) < 8:
            flash(
                "Yeni şifre en az 8 karakter olmalıdır.",
                "error"
            )

        elif new_password != new_password_repeat:
            flash(
                "Yeni şifreler uyuşmuyor.",
                "error"
            )

        else:
            password_hash = generate_password_hash(new_password)

            update_customer_password(
                customer_id,
                password_hash
            )

            flash(
                "Şifreniz başarıyla güncellendi.",
                "success"
            )

            return redirect(
                url_for("settings.change_password")
            )

    return render_template(
        "settings.html",
        customer=customer
    )