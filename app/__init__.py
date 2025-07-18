from flask import Flask
from flask_cors import CORS
from config import Config
from flask_migrate import Migrate  # 👈 tambahkan ini
from app.models import db  # ambil db dari models.py
from .project_routes import project_bp  # 👈 tambahkan ini
from .product_type_routes import product_type_bp

migrate = Migrate()  # 👈 inisialisasi migrate di luar fungsi

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)  # 👈 tambahkan ini

    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(product_type_bp)

    # with app.app_context():
    #     db.create_all()

    return app
