from flask import Blueprint, request, jsonify
from core.middlewares import login_required
from orders.models import Order, OrderItem
from .schemas import CreateOrderSchema

orders_bp = Blueprint("orders", __name__)


@orders_bp.route("/", methods=["POST"])
@login_required
def create_order():
    data = request.get_json()
    try:
        validated = CreateOrderSchema(**data)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    # quantity > 0, product_id > 0 tekshirish
    for item in validated.items:
        if item.product_id <= 0 or item.quantity <= 0:
            return (
                jsonify({"error": "product_id and quantity must be greater than 0"}),
                400,
            )
    return jsonify({"message": "Order created"})


# {
#     "orders": [
#         {
#             "product_variant_id": 1,
#             "quantity": 4,
#         }
#     ],
#     "address_id": 1,
# }


# Order api
# Cancel order api
# Get order by user id
# order detail id jonatadi, va shu id bilan order chiqariladi
