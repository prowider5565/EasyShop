from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
from core.middlewares import is_admin_user, login_required
from products.models import Product
from products.schemas import ProductSchema, RemoveSchema, UpdateSchema, PaginationSchema
from users.models import User
from users.schemas import UserSchema

product_bp = Blueprint("products", __name__)


@product_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
async def create():
    data = request.json
    try:
        product = ProductSchema(**data)
        try:
            user = await User.get(id=request.user["user_id"])
            product_obj = await Product.create(owner=user, **product.model_dump())
            return (
                jsonify(
                    {
                        "message": "Product created successfully",
                        "product_id": product_obj.id,
                    }
                ),
                201,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.delete("/remove/<int:product_id>")
@login_required
async def remove_product(product_id: int):
    try:
        try:
            product = await Product.get(id=product_id)
        except:
            return jsonify({"error": "Bunday product topilmadi"}), 404

        await product.delete()
        return {}, 204

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.route("/update/<int:product_id>", methods=["PATCH"])
@login_required
async def update_product(product_id: int):
    try:
        data = request.json

        update = UpdateSchema(**data)

        try:
            product = await Product.get(id=product_id)
        except:
            return jsonify({"error": "Mahsulot topilmadi"}), 404

        if update.name:
            product.name = update.name
        if update.description:
            product.description = update.description
        if update.price is not None:
            try:
                product.price = float(update.price)
            except:
                return jsonify({"error": "Narx raqam bo‘lishi kerak"}), 400

        await product.save()
        return jsonify({"message": "Mahsulot muvaffaqiyatli yangilandi"}), 200

    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.route("/list", methods=["POST"])
@login_required
async def get_products_paginated():
    data = request.get_json()

    try:
        pagination = PaginationSchema(**data)
        offset = (pagination.page - 1) * pagination.per_page

        total = await Product.all().count()
        products = (
            await Product.all()
            .offset(offset)
            .limit(pagination.per_page)
            .select_related("owner")
        )

        results = []
        for product in products:
            results.append(
                {
                    "id": product.id,
                    "name": product.name,
                    "description": product.description,
                    "price": product.price,
                    "owner": UserSchema.model_validate(product.owner).model_dump(),
                }
            )
        return jsonify(
            {
                "total": total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "products": results,
            }
        )
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@product_bp.get("/retrieve/<int:product_id>")
@login_required
async def get_one_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except DoesNotExist:
        return jsonify({"error": "Product not found"}), 404

    product_schema = ProductSchema.model_validate(product).model_dump()
    return jsonify(product_schema), 200
