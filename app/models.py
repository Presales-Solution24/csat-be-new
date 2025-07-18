from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_company = db.Column(db.String(255))
    nama_pribadi = db.Column(db.String(255))
    email = db.Column(db.String(255))
    no_hp = db.Column(db.String(50))
    jabatan = db.Column(db.String(255))
    project_title = db.Column(db.String(255))
    nama_presales = db.Column(db.String(255))
    tanggal_projek = db.Column(db.String(50))
    tanggal_approved = db.Column(db.String(50))
    approved = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    tipe_produk = db.Column(db.String(100))
    kategori_produk = db.Column(db.String(100))
    scoring_token = db.Column(db.String(64), unique=True, nullable=True)
    tasks = db.relationship("Task", backref="project", cascade="all, delete-orphan")

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey("project.id"))
    task = db.Column(db.String(255))
    expected_result = db.Column(db.String(255))
    actual_result = db.Column(db.String(255))

class ProductType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tipe_produk = db.Column(db.String(100), nullable=False)
    kategori_produk = db.Column(db.String(100), nullable=False)
