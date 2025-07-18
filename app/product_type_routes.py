from flask import Blueprint, request, jsonify
from app.models import db, ProductType

product_type_bp = Blueprint('product_type', __name__)

@product_type_bp.route("/product-types", methods=["GET"])
def get_all_product_types():
    types = ProductType.query.all()
    result = [
        {
            "id": t.id,
            "tipe_produk": t.tipe_produk,
            "kategori_produk": t.kategori_produk,
        }
        for t in types
    ]
    return jsonify(result), 200

@product_type_bp.route("/product-types", methods=["POST"])
def create_product_type():
    data = request.json
    new_type = ProductType(
        tipe_produk=data.get("tipe_produk"),
        kategori_produk=data.get("kategori_produk")
    )
    db.session.add(new_type)
    db.session.commit()
    return jsonify({
        "message": "Tipe produk berhasil ditambahkan",
        "id": new_type.id
    }), 201

@product_type_bp.route("/product-types/<int:id>", methods=["PUT"])
def update_product_type(id):
    data = request.json
    tipe = ProductType.query.get(id)
    if not tipe:
        return jsonify({"error": "Tipe produk tidak ditemukan"}), 404

    tipe.tipe_produk = data.get("tipe_produk", tipe.tipe_produk)
    tipe.kategori_produk = data.get("kategori_produk", tipe.kategori_produk)
    db.session.commit()
    return jsonify({"message": "Tipe produk berhasil diperbarui"}), 200

@product_type_bp.route("/product-types/<int:id>", methods=["DELETE"])
def delete_product_type(id):
    tipe = ProductType.query.get(id)
    if not tipe:
        return jsonify({"error": "Tipe produk tidak ditemukan"}), 404

    db.session.delete(tipe)
    db.session.commit()
    return jsonify({"message": "Tipe produk berhasil dihapus"}), 200

@product_type_bp.route("/product-types/<int:id>", methods=["GET"])
def get_product_type(id):
    tipe = ProductType.query.get(id)
    if not tipe:
        return jsonify({"error": "Tipe produk tidak ditemukan"}), 404

    return jsonify({
        "id": tipe.id,
        "tipe_produk": tipe.tipe_produk,
        "kategori_produk": tipe.kategori_produk
    }), 200
