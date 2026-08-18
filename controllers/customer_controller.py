from flask import Blueprint, flash, redirect, render_template, session, url_for

from controllers.auth_controller import login_required
from models.customer import get_customer_by_id


customer_bp = Blueprint("customer", __name__)


@customer_bp.route("/")
def home():

    if session.get("customer_id"):
        return redirect(url_for("customer.dashboard"))

    return redirect(url_for("auth.login"))


@customer_bp.route("/dashboard")
@login_required
def dashboard(customer):
    return render_template(
        "dashboard.html",
        customer=customer
    )