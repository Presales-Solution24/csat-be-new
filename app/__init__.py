from flask import Flask
from flask_cors import CORS
from config import Config
from app.models import db  # ambil db dari models.py
from .project_routes import project_bp  # 👈 tambahkan ini

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    db.init_app(app)

    from .auth_routes import auth_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(project_bp)

    with app.app_context():
        db.create_all()

    return app
