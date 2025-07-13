from flask import Blueprint, request, jsonify
from app.models import db, User
from app.utils.hash import hash_password, verify_password

auth_api_blueprint = Blueprint('auth_api', __name__)

@auth_api_blueprint.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Semua field wajib diisi."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Username atau email sudah digunakan."}), 400

    user = User(username=username, email=email, password=hash_password(password))
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Register berhasil."}), 201

@auth_api_blueprint.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not verify_password(password, user.password):
        return jsonify({"message": "Username atau password salah."}), 401

    return jsonify({"message": "Login berhasil", "username": user.username}), 200
