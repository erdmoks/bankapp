import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf.csrf import CSRFProtect

from database import init_db, close_db
from controllers.auth_controller import auth_bp
from controllers.customer_controller import customer_bp
from controllers.settings_controller import settings_bp
from controllers.transfer_controller import transfer_bp

from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv() 

csrf = CSRFProtect()

def create_app():

    app = Flask(__name__)
    csrf.init_app(app)
    app.wsgi_app = ProxyFix(
        app.wsgi_app,
        x_for=1
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    app.teardown_appcontext(close_db)

    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(settings_bp)
    app.register_blueprint(transfer_bp)

    with app.app_context():
        init_db()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )