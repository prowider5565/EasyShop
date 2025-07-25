from flask import Blueprint, request, jsonify
from core.middlewares import login_required
from models.orders import Order, ItemSet
from sqlalchemy.orm import Session
from collections import defaultdict
from core.database import SessionLocal

orders_bp = Blueprint("orders", __name__)


session: Session = SessionLocal()
# @orders_bp.route("/orders", methods=["POST"])
# @login_required
# def create_order():
#     data = request.get_json()

#     address_id = data.get("address_id")
#     order_items = data.get("orders")

#     if not address_id or not order_items:
#         return jsonify({"error": "Missing address_id or orders"}), 400

#     try:
#         # customer_id ni g.current_user.id dan olamiz
#         order = Order(
#             address_id=address_id,
#             customer_id=g.current_user.id
#         )
#         session.add(order)
#         session.flush()  # order.id olish uchun

#         for item in order_items:
#             order_item = OrderItem(
#                 order_id=order.id,
#                 product_variant_id=item["product_variant_id"],
#                 quantity=item["quantity"]
#             )
#             session.add(order_item)

#         session.commit()
#         return jsonify({"message": "Order created", "order_id": order.id}), 201

#     except Exception as e:
#         session.rollback()
#         return jsonify({"error": str(e)}), 500

@orders_bp.route("/create", methods=["POST"])
def create_order():
    session = SessionLocal()
    data = request.get_json()

    try:
        # Order yaratish
        order = Order(address_id=data["address_id"])
        session.add(order)
        session.commit()  # order.id kerak bo'ladi itemlarga

        # Bir xil product_variant_id larni quantity bo‘yicha jamlash
        combined_items = defaultdict(int)
        for item in data["orders"]:
            combined_items[item["product_variant_id"]] += item["quantity"]

        # ItemSet larni yaratish
        for variant_id, quantity in combined_items.items():
            itemset = ItemSet(
                product_variant_id=variant_id,
                quantity=quantity,
                order_id=order.id
            )
            session.add(itemset)

        session.commit()

        return jsonify({"message": "Order created", "order_id": order.id})

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        session.close()

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
