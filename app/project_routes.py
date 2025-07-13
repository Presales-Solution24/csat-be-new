from flask import Blueprint, request, jsonify
from app.models import db, Project, Task
from datetime import datetime

project_bp = Blueprint('project_bp', __name__)

@project_bp.route('/project-satisfaction', methods=['POST'])
def save_project_satisfaction():
    data = request.get_json()
    project_id = data.get('project_id')

    try:
        if project_id:
            project = Project.query.get(project_id)
            if not project:
                return jsonify({'error': 'Project not found'}), 404
            # Update existing project
            project.nama_company = data.get('namaCompany')
            project.nama_pribadi = data.get('namaPribadi')
            project.email = data.get('email')
            project.no_hp = data.get('noHp')
            project.jabatan = data.get('jabatan')
            project.project_title = data.get('projectTitle')
            project.nama_presales = data.get('namaPresales')
            project.tanggal_projek = data.get('tanggalProjek')
            project.tanggal_approved = data.get('tanggalApproved')
            project.approved = data.get('approved')
            project.rating = data.get('rating')
            project.tipe_produk = data.get('tipeProduk')
            project.kategori_produk = data.get('kategoriProduk')
            
            # Hapus semua task lama
            Task.query.filter_by(project_id=project_id).delete()
        else:
            # Buat project baru
            project = Project(
                nama_company=data.get('namaCompany'),
                nama_pribadi=data.get('namaPribadi'),
                email=data.get('email'),
                no_hp=data.get('noHp'),
                jabatan=data.get('jabatan'),
                project_title=data.get('projectTitle'),
                nama_presales=data.get('namaPresales'),
                tanggal_projek=data.get('tanggalProjek'),
                tanggal_approved=data.get('tanggalApproved'),
                approved=data.get('approved'),
                rating=data.get('rating'),
                tipe_produk=data.get('tipeProduk'),
                kategori_produk=data.get('kategoriProduk'),
            )
            db.session.add(project)
            db.session.flush()  # agar project.id langsung tersedia

        # Simpan task-task baru
        tasks = data.get('tasks', [])
        for t in tasks:
            task = Task(
                project_id=project.id,
                task=t.get('task'),
                expected_result=t.get('expectedResult'),
                actual_result=t.get('actualResult')
            )
            db.session.add(task)

        db.session.commit()
        return jsonify({"message": "Project saved", "project_id": project.id}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@project_bp.route('/project-satisfaction/<int:id>', methods=['GET'])
def get_project_satisfaction(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    tasks = Task.query.filter_by(project_id=id).all()

    return jsonify({
        "namaCompany": project.nama_company,
        "namaPribadi": project.nama_pribadi,
        "email": project.email,
        "noHp": project.no_hp,
        "jabatan": project.jabatan,
        "projectTitle": project.project_title,
        "namaPresales": project.nama_presales,
        "tanggalProjek": str(project.tanggal_projek),
        "tanggalApproved": str(project.tanggal_approved),
        "approved": project.approved,
        "rating": project.rating,
        "tipeProduk": project.tipe_produk,
        "kategoriProduk": project.kategori_produk,
        "tasks": [
            {
                "task": t.task,
                "expectedResult": t.expected_result,
                "actualResult": t.actual_result
            }
            for t in tasks
        ]
    })