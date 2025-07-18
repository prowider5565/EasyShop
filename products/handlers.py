from flask import Blueprint, request, jsonify
from sqlalchemy.orm import Session, joinedload
from pydantic import ValidationError
from core.middlewares import login_required, is_admin_user
from products.schemas import ProductSchema, UpdateSchema, PaginationSchema
from products.models import Product
from category.models import Category
from users.models import User
from users.schemas import UserSchema
from core.settings import SessionLocal

product_bp = Blueprint("products", __name__)

# 1. Tovarlarga category qushish, va cateogry bilan productni boglash foreignkey bilan - DONE
# 2. product list apida filter qushish date order by - DONE, name bilan search - DONE, owner id bilan filter qilish - DONE, by category filter - DONE
# 3. order qila olsh, yani bir nechta mahsulotlar zakaz qilish mumkin, va har bir zakazni miqdori bulishi kerak


@product_bp.route("/create", methods=["POST"])
@login_required
@is_admin_user
def create_product():
    data = request.get_json()
    try:
        validated = ProductSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        user = session.query(User).get(request.user["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        category = session.query(Category).get(validated.category_id)
        if not category:
            return jsonify({"error": "Category not found"}), 404

        product = Product(
            name=validated.name,
            description=validated.description,
            price=validated.price,
            owner_id=user.id,
            category_id=category.id,
            in_stock=validated.in_stock or 0,
        )
        session.add(product)
        session.commit()
        return jsonify({"message": "Product created", "product_id": product.id}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@product_bp.route("/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_product(product_id: int):
    session: Session = SessionLocal()
    try:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404
        session.delete(product)
        session.commit()
        return "", 204
    finally:
        session.close()


@product_bp.route("/update/<int:product_id>", methods=["PATCH"])
@login_required
def update_product(product_id: int):
    data = request.get_json()
    try:
        validated = UpdateSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        product = session.query(Product).get(product_id)
        if not product:
            return jsonify({"error": "Product not found"}), 404

        if validated.name is not None:
            product.name = validated.name
        if validated.description is not None:
            product.description = validated.description
        if validated.price is not None:
            product.price = validated.price

        session.commit()
        return jsonify({"message": "Product updated"}), 200
    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        session.close()


@product_bp.route("/list", methods=["POST"])
@login_required
def get_products_paginated():
    data = request.get_json()
    try:
        pagination = PaginationSchema(**data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    session: Session = SessionLocal()
    try:
        total = session.query(Product).count()
        products = (
            session.query(Product)
            .options(joinedload(Product.owner))
            .offset((pagination.page - 1) * pagination.per_page)
            .limit(pagination.per_page)
            .all()
        )
        result = []
        for p in products:
            result.append(
                {
                    "id": p.id,
                    "name": p.name,
                    "description": p.description,
                    "price": p.price,
                    "owner": UserSchema.model_validate(p.owner).model_dump(),
                    # "category": ProductSchema.model_validate(product.category).model_dump(),
                }
            )
        return jsonify(
            {
                "total": total,
                "page": pagination.page,
                "per_page": pagination.per_page,
                "products": result,
            }
        )
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

@product_bp.get("/date_order")
@login_required
async def get_sorted_products():
    products = await Product.all().order_by("created_at")

    if not products:
        return jsonify({"error": "Mahsulotlar topilmadi"}), 404

    result = []
    for product in products:
        result.append({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category,
            "created_at": product.created_at.isoformat()
        })

    return jsonify(result), 200

@product_bp.get("/search/<string:name>")
@login_required
async def get_product_name(name: str):
    try:    
        products = await Product.filter(name=name).all()
    except Exception as e:
        return jsonify({"error": "Product not found"})

    result = []
    for product in products:
            result.append({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category
        })
    return jsonify(result)

@product_bp.get("/find/<int:own_id>")
@login_required
async def get_by_owner_id(own_id:int):
    owners = await Product.filter(owner_id=own_id).all() 

    if not owners:
        return jsonify({"error": "Products not found"}), 404
    
    result = []
    for product in owners:
        result.append({
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "category": product.category
        })
    return jsonify(result)

@product_bp.get("/retrieve/<int:product_id>")
@login_required
async def get_one_product(product_id: int):
    try:
        product = await Product.get(id=product_id)
    except Exception:
        return jsonify({"error": "Product not found"}), 404

    product_schema = ProductSchema.model_validate(product).model_dump()
    return jsonify(product_schema), 200
