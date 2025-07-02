from flask import Flask
from tortoise import run_async

from core.utils import init_db


app = Flask(__name__)


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


@app.get("/hello")
def say_hello():
    return {"msg": "Hello Pythonic world!"}


if __name__ == "__main__":
    run_async(init_db())
    app.run(debug=True, port=3030)
