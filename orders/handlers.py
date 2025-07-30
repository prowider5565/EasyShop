from flask import Blueprint, request, jsonify
from core.middlewares import login_required
from models.orders import Order, ItemSet
import stripe
from sqlalchemy.orm import Session
from .schemas import CreateOrderSchema
from collections import defaultdict
from models.variants import Variant
from core.database import SessionLocal

orders_bp = Blueprint("orders", __name__)


session: Session = SessionLocal()


@orders_bp.route("/create", methods=["POST"])
def create_order():
    session = SessionLocal()
    data = request.get_json()

    try:
        # 1. Create Order
        order = Order(address_id=data["address_id"])
        session.add(order)
        session.commit()

        # 2. Combine items
        combined_items = defaultdict(int)
        for item in data["orders"]:
            combined_items[item["product_variant_id"]] += item["quantity"]

        # 3. Create ItemSets and calculate Stripe line_items
        line_items = []
        for variant_id, quantity in combined_items.items():
            variant = session.query(Variant).get(variant_id)
            if not variant:
                raise Exception(f"Variant {variant_id} not found")

            itemset = ItemSet(
                product_variant_id=variant_id, quantity=quantity, order_id=order.id
            )
            session.add(itemset)

            line_items.append(
                {
                    "price_data": {
                        "currency": "usd",
                        "unit_amount": int(variant.price * 100),
                        "product_data": {"name": variant.name},
                    },
                    "quantity": quantity,
                }
            )

        session.commit()

        # 4. Create Stripe Checkout Session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=line_items,
            success_url="https://c941d7dfe82a.ngrok-free.app/api/welcome-page",  # update this
            cancel_url="https://facebook.com",
            metadata={"order_id": order.id},
        )

        return jsonify(
            {
                "message": "Order created",
                "order_id": order.id,
                "payment_url": checkout_session.url,
            }
        )

    except Exception as e:
        session.rollback()
        return jsonify({"error": str(e)}), 400

    finally:
        session.close()
