import jwt
import datetime
from flask import Blueprint, request, jsonify, current_app
from . import db
from .models import User
from passlib.hash import sha256_crypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"message": "Semua field wajib diisi."}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"message": "Username atau email sudah digunakan."}), 400

    hashed_pw = sha256_crypt.hash(password)
    user = User(username=username, email=email, password=hashed_pw)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Register berhasil."}), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not sha256_crypt.verify(password, user.password):
        return jsonify({"message": "Username atau password salah."}), 401

    # Buat JWT token dengan expiration 1 bulan
    token_payload = {
        "user_id": user.id,
        "username": user.username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=30)  # Expired dalam 30 hari
    }

    token = jwt.encode(token_payload, current_app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({
        "message": "Login berhasil.",
        "username": user.username,
        "token": token
    }), 200
