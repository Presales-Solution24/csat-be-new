from flask import Blueprint, request, jsonify
from app.models import db, ProjectSatisfaction

project_bp = Blueprint('project', __name__)

@project_bp.route('/project-satisfaction', methods=['POST'])
def save_project_satisfaction():
    data = request.get_json()

    # Manual assignment dari JSON ke kolom model
    project = ProjectSatisfaction(
        nama_company = data.get("namaCompany"),
        nama_pribadi = data.get("namaPribadi"),
        email = data.get("email"),
        no_hp = data.get("noHp"),
        jabatan = data.get("jabatan"),
        project_title = data.get("projectTitle"),
        nama_presales = data.get("namaPresales"),
        tanggal_projek = data.get("tanggalProjek"),
        tanggal_approved = data.get("tanggalApproved"),
        approved = data.get("approved"),
        rating = data.get("rating"),
        tipe_produk = data.get("tipeProduk"),
        kategori_produk = data.get("kategoriProduk"),
        task = data.get("task"),
        expected_result = data.get("expectedResult"),
        actual_result = data.get("actualResult"),
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({"message": "Data berhasil disimpan"}), 201
