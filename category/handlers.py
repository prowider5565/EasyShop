from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session, joinedload
from core.middlewares import is_admin_user, login_required
from category.schemas import CategorySchema
from category.models import Category
from core.settings import SessionLocal

category_bp = Blueprint("category", __name__)

@category_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
def category_create():
    data = request.get_json()
    try:
        validated = CategorySchema(**data)
    except Exception as e:
        return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

    session: Session = SessionLocal()
    try:
        category = Category(name=validated.name)
        session.add(category)
        session.commit()
        return jsonify({"message": "Category created successfully", "id": category.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()

@category_bp.route("/id/<int:category_id>", methods=["GET"])
@login_required
def get_products_by_category(category_id: int):
    session: Session = SessionLocal()
    try:
        category = (
            session.query(Category)
                   .options(joinedload(Category.products))
                   .filter_by(id=category_id)
                   .one_or_none()
        )
        if category is None:
            return jsonify({"error": "Category not found"}), 404

        data = {
            "category_id": category.id,
            "name": category.name,
            "products": [
                {"id": p.id, "name": p.name}
                for p in category.products
            ],
        }
        return jsonify(data), 200
    finally:
        session.close()

# Category delete
# Category Update
# Category list
