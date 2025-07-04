# CRUD  - create_product, remove_product, update_product, delete_product


from flask import Blueprint, request, jsonify
from products.models import Product

product_bp = Blueprint("products", __name__)

@product_bp.route("/create", methods=["POST"])
async def register():
    data = request.form

    product_name = data.get("name")
    product_description = data.get("description")
    product_price = data.get("price")

    if not product_name or not product_description or not product_price:
        return jsonify({"error": "All fields are required"}), 400


    try:
        await Product.create(product_name = product_name, product_description = product_description, product_price = product_price)
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

