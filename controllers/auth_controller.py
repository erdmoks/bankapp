from datetime import datetime
from functools import wraps
import html
import random

import sqlite3

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from models.customer import create_customer, get_customer_by_email, get_customer_by_id
from models.session import increment_and_get_session_version, increment_session_version

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if session.get("customer_id"):
        return redirect(url_for("customer.dashboard"))

    if request.method == "POST":

        first_name = html.escape(request.form.get("first_name", "").strip())
        last_name = html.escape(request.form.get("last_name", "").strip())
        email = request.form.get("email", "").strip().lower()
        phone = html.escape(request.form.get("phone", "").strip())
        birth_date = html.escape(request.form.get("birth_date", ""))
        password = request.form.get("password", "")
        password_repeat = request.form.get("password_repeat", "")

        if not all([
            first_name,
            last_name,
            email,
            phone,
            birth_date,
            password
        ]):
            flash("Lütfen tüm alanları doldurun.", "error")

        elif "@" not in email:
            flash("Geçerli bir e-posta adresi yazın.", "error")

        elif len(password) < 8:
            # Regex kontrolü eklenecek!
            flash("Şifre en az 8 karakter olmalıdır.", "error")

        elif password != password_repeat:
            flash("Şifreler uyuşmuyor.", "error")

        else:
            max_retries = 5
            registered = False

            for attempt in range(max_retries):
                customer_id = str(random.randint(10000, 99999))

                try:
                    create_customer(
                        customer_id,
                        first_name,
                        last_name,
                        email,
                        phone,
                        birth_date,
                        generate_password_hash(password),
                        datetime.now().isoformat(timespec="seconds")
                    )
                    registered = True
                    break

                except sqlite3.IntegrityError as e:
                    if "customer_id" in str(e):
                        continue  
                    else:
                        flash("Bu e-posta adresi zaten kayıtlı.", "error")
                        break

            if registered:
                flash(
                    "Kaydınız oluşturuldu. Şimdi giriş yapabilirsiniz.",
                    "success"
                )
                return redirect(url_for("auth.login"))
            elif not registered and attempt == max_retries - 1:
                flash(
                    "Bir hata oluştu, lütfen tekrar deneyin.",
                    "error"
                )

    return render_template("register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if session.get("customer_id"):
        return redirect(url_for("customer.dashboard"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        customer = get_customer_by_email(email)

        if customer and check_password_hash(
            customer["password_hash"],
            password
        ):
            new_session_version = increment_and_get_session_version(
                customer["customer_id"]
            )

            session.clear()
            session["customer_id"] = customer["customer_id"]
            session["session_version"] = new_session_version

            flash(
                "Hoş geldiniz, {}!".format(customer["first_name"]),
                "success"
            )

            return redirect(url_for("customer.dashboard"))

        flash("Giriş bilgileriniz hatalı!", "error")
        return render_template("login.html"), 401

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    increment_session_version(session.get("customer_id"))
    session.clear()

    flash(
        "Güvenli şekilde çıkış yaptınız.",
        "success"
    )

    return redirect(url_for("auth.login"))

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        customer_id = session.get("customer_id")
        session_version = session.get("session_version")


        if not customer_id or session_version is None:
            session.clear()

            flash("Lütfen Giriş Yapınız !", "error")
            return redirect(url_for("auth.login"))

        customer = get_customer_by_id(customer_id)

        if not customer:
            session.clear()
            flash("Oturumunuz geçersiz. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for("auth.login"))

        if customer["session_version"] != session_version:
            session.clear()
            flash("Oturumunuz geçersiz. Lütfen tekrar giriş yapın.", "error")
            return redirect(url_for("auth.login"))
        
        return f(customer, *args, **kwargs)

    return decorated_function
