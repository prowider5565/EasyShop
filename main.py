from flask import Flask
from users.handlers import user_bp
from payment.handlers import stripe_bp
from products.handlers import product_bp
from category.handlers import category_bp
from orders.handlers import orders_bp
from products.variants.handlers import variants_bp
from identity.handlers import addr_router

"""
Backend dasturlashda quyidagi http metodlar bor:
    GET  - Ma'lumotlarni backenddan olib beradi.
    POST - Ma'lumotni backendga jo'natadi, ushbu ma'lumot backendni vazifasiga qarab obrabotka boladi
        Misol uchun:
            Foydalanuvchi qoshish uchun:
                {
                    "username": "Something",
                    "password": "9999"
                }
    PATCH  - Ma'lumotni ozgartiradi qisman
    PUT    - Ma'lumotni ozgartiradi qo'liq
    DELETE - Ma'lumotni ochirib tashlaydi

"""


app = Flask(__name__)

app.register_blueprint(user_bp, url_prefix="/users")
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(category_bp, url_prefix="/category")
app.register_blueprint(orders_bp, url_prefix="/orders")
app.register_blueprint(variants_bp, url_prefix="/variants")
app.register_blueprint(addr_router, url_prefix="/address")
app.register_blueprint(stripe_bp, url_prefix="/stripe")
if __name__ == "__main__":
    app.run(debug=True)
