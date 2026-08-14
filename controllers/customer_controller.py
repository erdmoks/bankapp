from flask import Blueprint, flash, redirect, render_template, session, url_for

from models.customer import get_customer_by_id


customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/")
def home():

    if session.get("customer_id"):
        return redirect(url_for("customer.dashboard"))

    return redirect(url_for("auth.login"))


@customer_bp.route("/dashboard")
def dashboard():

    customer_id = session.get("customer_id")

    if not customer_id:
        flash(
            "Devam etmek için giriş yapın.",
            "error"
        )

        return redirect(url_for("auth.login"))

    customer = get_customer_by_id(customer_id)

    if customer is None:
        session.clear()
        return redirect(url_for("auth.login"))

    return render_template(
        "dashboard.html",
        customer=customer
    )