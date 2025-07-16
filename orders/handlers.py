from flask import Blueprint, request, jsonify
from orders.models import Order, OrderItem
from .schemas import CreateOrderSchema

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['POST'])
def create_order():
    data = request.get_json()
    try:
        validated = CreateOrderSchema(**data)
        try:
            product_obj = Order.create(**validated.model_dump())
            return jsonify({'message': 'Order created'})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 400

    # quantity > 0, product_id > 0 tekshirish
    # for item in validated.items:
    #     if item.product_id <= 0 or item.quantity <= 0:
    #         return jsonify({'error': 'product_id and quantity must be greater than 0'}), 400

    # bu yerda tortoise-orm create qilish asosan async bo‘ladi.
    # Flask async route ishlatmayapti, shuning uchun bu qismda `async` ishlatolmaymiz.
    # To'g'ri ishlashi uchun `async` qismni alohida event loop ichida bajarish yoki sync qilib yozish kerak.
    # Kichkina loyiha uchun oddiy create qilishni sync yozib tur:
    
    # Pseudokod:
    # order = Order.create_sync() yoki
    # loop = asyncio.get_event_loop()
    # order = loop.run_until_complete(Order.create())



