from ..utils.db import db
from datetime import datetime

class ProjectSatisfaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    # Customer Info
    nama_company = db.Column(db.String(100))
    nama_pribadi = db.Column(db.String(100))
    email = db.Column(db.String(100))
    no_hp = db.Column(db.String(50))
    jabatan = db.Column(db.String(100))

    # Project Info
    project_title = db.Column(db.String(150))
    nama_presales = db.Column(db.String(100))
    tanggal_projek = db.Column(db.Date)
    tanggal_approved = db.Column(db.Date)
    approved = db.Column(db.String(10))
    rating = db.Column(db.String(10))
    tipe_produk = db.Column(db.String(100))
    kategori_produk = db.Column(db.String(100))

    # Task Info
    task = db.Column(db.String(255))
    expected_result = db.Column(db.Text)
    actual_result = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
