# CRUD  - create_product(product_owner)-done, remove_product-done, update_product - done


from flask import Blueprint, request, jsonify
from products.models import Product
from users.models import User

product_bp = Blueprint("products", __name__)

@product_bp.route("/create", methods=["POST"])
async def create():
    data = request.form

    product_name = data.get("name")
    product_description = data.get("description")
    product_price = data.get("price")
    product_owner_id = data.get("owner")

    if not product_name or not product_description or not product_price:
        return jsonify({"error": "All fields are required"}), 400


    try:
        await Product.create(product_name = product_name, product_description = product_description, product_price = product_price,product_owner_id = product_owner_id)
        return jsonify({"message": "Product created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@product_bp.route("/remove", methods=["POST"])
async def remove_product():
    data = request.form

    product_owner_id = data.get("owner_id")
    product_id = data.get("id")

    if not product_owner_id or not product_id:
        return jsonify({"error": "All fields are required"}), 400

    try:
        product = await Product.get(id=int(product_id))
    except:
        return jsonify({"error": "Bunday product topilmadi"}), 404

    if str(product.product_owner_id) != product_owner_id:
        return jsonify({"error": "Siz bu product egasi emassiz!"}), 403

    await product.delete()
    return jsonify({"message": "Product muvaffaqiyatli o'chirildi"}), 200

@product_bp.route("/update", methods=["POST"])
async def update_product():
    data = request.form

    product_id = data.get("id")
    owner_id = data.get("owner_id")
    name = data.get("name")
    description = data.get("description")
    price = data.get("price")

    if not product_id or not owner_id:
        return jsonify({"error": "ID va egasi kerak"}), 400

    try:
        product = await Product.get(id=int(product_id))
    except:
        return jsonify({"error": "Mahsulot topilmadi"}), 404

    if str(product.product_owner_id) != owner_id:
        return jsonify({"error": "Siz bu product egasi emassiz!"}), 403

    if name:
        product.product_name = name
    if description:
        product.product_description = description
    if price:
        try:
            product.product_price = int(price)
        except:
            return jsonify({"error": "Narx raqam bo‘lishi kerak"}), 400

    await product.save()
    return jsonify({"message": "Mahsulot muvaffaqiyatli yangilandi"}), 200