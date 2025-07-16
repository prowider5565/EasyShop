from flask import Blueprint, request, jsonify
from core.middlewares import is_admin_user, login_required
from tortoise.exceptions import DoesNotExist
from category.schemas import CategorySchemas
from category.models import Category

category_bp = Blueprint("category", __name__)


@category_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
async def category_create():
    data = request.json
    try:
        try:
            category = CategorySchemas(**data)
            product_obj = await Category.create(**category.model_dump())
            return jsonify({"message": "Succesfully category created!"})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@category_bp.get("/id/<int:category_id>")
@login_required
async def get_products_by_category(category_id):
    try:
        category = await Category.get(id=category_id).prefetch_related('products')
        data = {
            "category_id": category.id,
            "name": category.name,
            "products": [{"id": p.id, "name": p.name} for p in category.products]
        }
        return jsonify(data)
    except:
        return jsonify({"error": "Category not found"}), 404
