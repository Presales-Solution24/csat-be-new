from flask import Blueprint, request, jsonify
from app.models import db, Project, Task
from datetime import datetime
import secrets

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

            # Jika token belum ada, generate
            if not project.scoring_token:
                project.scoring_token = secrets.token_urlsafe(32)

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
                scoring_token=secrets.token_urlsafe(32)  # generate token
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
        "scoring_token": project.scoring_token,
        "tasks": [
            {
                "task": t.task,
                "expectedResult": t.expected_result,
                "actualResult": t.actual_result
            }
            for t in tasks
        ]
    })


@project_bp.route('/project-satisfaction', methods=['GET'])
def list_project_satisfaction():
    projects = Project.query.order_by(Project.id.desc()).all()
    result = []
    for project in projects:
        tasks = Task.query.filter_by(project_id=project.id).all()
        result.append({
            "id": project.id,
            "nama_company": project.nama_company,
            "nama_pribadi": project.nama_pribadi,
            "email": project.email,
            "no_hp": project.no_hp,
            "jabatan": project.jabatan,
            "project_title": project.project_title,
            "nama_presales": project.nama_presales,
            "tanggal_projek": str(project.tanggal_projek) if project.tanggal_projek else None,
            "tanggal_approved": str(project.tanggal_approved) if project.tanggal_approved else None,
            "approved": project.approved,
            "rating": project.rating,
            "tipe_produk": project.tipe_produk,
            "kategori_produk": project.kategori_produk,
            "tasks": [
                {
                    "id": task.id,
                    "project_id": task.project_id,
                    "task_name": task.task,
                    "expected_result": task.expected_result,
                    "actual_result": task.actual_result
                } for task in tasks
            ]
        })
    return jsonify(result)


@project_bp.route('/project-satisfaction/<int:id>', methods=['DELETE'])
def delete_project_satisfaction(id):
    try:
        project = Project.query.get(id)
        if not project:
            return jsonify({"error": "Project not found"}), 404

        # Hapus semua task terkait
        Task.query.filter_by(project_id=id).delete()

        # Hapus project
        db.session.delete(project)
        db.session.commit()

        return jsonify({"message": "Project and related tasks deleted successfully."}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@project_bp.route('/public-scoring/<token>', methods=['GET'])
def get_project_by_token(token):
    project = Project.query.filter_by(scoring_token=token).first()
    if not project:
        return jsonify({"error": "Invalid or expired token"}), 404

    tasks = Task.query.filter_by(project_id=project.id).all()

    return jsonify({
        "id": project.id,
        "nama_company": project.nama_company,
        "nama_pribadi": project.nama_pribadi,
        "email": project.email,
        "no_hp": project.no_hp,
        "jabatan": project.jabatan,
        "project_title": project.project_title,
        "nama_presales": project.nama_presales,
        "tanggal_projek": project.tanggal_projek,
        "tanggal_approved": project.tanggal_approved,
        "approved": project.approved,
        "rating": project.rating,
        "tipe_produk": project.tipe_produk,
        "kategori_produk": project.kategori_produk,
        "tasks": [
            {
                "task": t.task,
                "expected_result": t.expected_result,
                "actual_result": t.actual_result
            }
            for t in tasks
        ]
    })

@project_bp.route('/public-scoring/<token>', methods=['POST'])
def update_project_scoring_by_token(token):
    project = Project.query.filter_by(scoring_token=token).first()
    if not project:
        return jsonify({"error": "Invalid or expired token"}), 404

    data = request.get_json()
    project.tanggal_approved = data.get("tanggal_approved", "")
    project.approved = data.get("approved", "")
    project.rating = data.get("rating", "")

    db.session.commit()
    return jsonify({"message": "Scoring updated successfully"})
