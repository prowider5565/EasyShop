from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session, joinedload
from core.middlewares import is_admin_user, login_required
from category.schemas import WriteCategorySchema
from models.categories import Category
from core.database import SessionLocal

category_bp = Blueprint("category", __name__)


@category_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
def category_create():
    data = request.get_json()
    try:
        validated = WriteCategorySchema(**data)
    except Exception as e:
        return jsonify({"error": e.errors() if hasattr(e, "errors") else str(e)}), 400

    session: Session = SessionLocal()
    try:
        category = Category(name=validated.name)
        session.add(category)
        session.commit()
        return (
            jsonify({"message": "Category created successfully", "id": category.id}),
            201,
        )
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
            "products": [{"id": p.id, "name": p.name} for p in category.products],
        }
        return jsonify(data), 200
    finally:
        session.close()

# DELETE CATEGORY
@category_bp.route("/delete/<int:category_id>", methods=["DELETE"])
@login_required
@is_admin_user
def delete_category(category_id):
    session: Session = SessionLocal()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        session.delete(category)
        session.commit()
        return jsonify({"message": "Category deleted successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# UPDATE CATEGORY
@category_bp.route("/update/<int:category_id>", methods=["PUT"])
@login_required
@is_admin_user
def update_category(category_id):
    data = request.get_json()
    session: Session = SessionLocal()
    try:
        category = session.query(Category).get(category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        validated = WriteCategorySchema(**data)
        category.name = validated.name
        session.commit()
        return jsonify({"message": "Category updated successfully"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


# LIST ALL CATEGORIES
@category_bp.route("/all", methods=["GET"])
@login_required
def list_all_categories():
    session: Session = SessionLocal()
    try:
        categories = session.query(Category).all()
        result = [{"id": c.id, "name": c.name} for c in categories]
        return jsonify(result), 200
    finally:
        session.close()
        