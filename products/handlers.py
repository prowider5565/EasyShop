from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from tortoise.exceptions import DoesNotExist
from core.middlewares import is_admin_user, login_required
from products.models import Product
from category.models import Category
from products.schemas import ProductSchema, UpdateSchema, PaginationSchema
from users.models import User
from users.schemas import UserSchema
# from category.models import Category
# from datetime import datetime

product_bp = Blueprint("products", __name__)

# 1. Tovarlarga category qushish, va cateogry bilan productni boglash foreignkey bilan - DONE
# 2. product list apida filter qushish date order by - DONE, name bilan search - DONE, owner id bilan filter qilish - DONE, by category filter - DONE
# 3. order qila olsh, yani bir nechta mahsulotlar zakaz qilish mumkin, va har bir zakazni miqdori bulishi kerak


@product_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
async def create():
    data = request.json
    try:
        product_data = ProductSchema(**data)

        try:
            user = await User.get(id=request.user["user_id"])

            # Kategoriya mavjudligini tekshirish
            category = await Category.get_or_none(id=product_data.category_id)
            if not category:
                return jsonify({"error": "Category not found"}), 404

            # Mahsulotni yaratish
            product_obj = await Product.create(
                # name=product_data.name,
                owner=user,
                category=category,
                **product_data.model_dump()
                # boshqa maydonlar bo‘lsa shu yerda yozing
            )

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
                    # "category": ProductSchema.model_validate(product.category).model_dump(),
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

# @product_bp.get("/category/<int:category_id>")
# @login_required
# async def get_products_by_category(category_id):
#     try:
#         category = await Category.get(id=category_id).prefetch_related('products')
#         # category.products bu related_name orqali bog‘langan productlar
#         data = {
#             "category_id": category.id,
#             "name": category.name,
#             "products": [{"id": p.id, "name": p.name} for p in category.products]
#         }
#         return jsonify(data)
#     except:
#         return jsonify({"error": "Category not found"}), 404


# 3. order qila olsh, yani bir nechta mahsulotlar zakaz qilish mumkin, va har bir zakazni miqdori bulishi kerak

# @product_bp.get("/order")
# @login_required
# async def buy_order():
#     data = request.json




@product_bp.get("/date_order")
@login_required
async def get_sorted_products():
    products = await Product.all().select_related("category").order_by("created_at")

    if not products:
        return jsonify({"error": "Mahsulotlar topilmadi"}), 404

    result = []
    for product in products:
        result.append({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category.name,  # bu endi ishlaydi
            "created_at": product.created_at.isoformat()
        })

    return jsonify(result), 200

@product_bp.get("/search/<string:name>")
@login_required
async def get_product_name(name: str):
    try:    
        products = await Product.filter(name=name).select_related("category").all()
        if not products:
            return jsonify({"error": "Product not found"}), 404
        result = []
        for product in products:
            result.append({
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "category": product.category.name
            })
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@product_bp.get("/find/<int:own_id>")
@login_required
async def get_by_owner_id(own_id: int):
    owners = await Product.filter(owner=own_id).select_related("category").all()

    if not owners:
        return jsonify({"error": "Products not found"}), 404

    result = []
    for product in owners:
        result.append({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category.name,
        })
    return jsonify(result), 200

@product_bp.get("/retrieve/<int:product_id>")
@login_required
async def get_one_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except DoesNotExist:
        return jsonify({"error": "Product not found"}), 404

    product_schema = ProductSchema.model_validate(product).model_dump()
    return jsonify(product_schema), 200
