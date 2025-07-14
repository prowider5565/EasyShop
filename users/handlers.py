from flask import Blueprint, request, jsonify
from users.models import User

# from core.utils import hash_password
import hashlib
from users.schemas import RegisterSchema, LoginSchema, GetSchema
from pydantic import ValidationError

from utils.auth import hash_password, verify_password
from utils.jwt import full_jwt


user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["POST"])
async def register():
    data = request.json

    try:
        user = RegisterSchema(**data)
        user.password = hash_password(user.password)
        try:
            new_user = await User.create(**user.model_dump())
            return (
                jsonify(
                    {
                        "message": "Ro'yxatdan muvaffaqiyatli o'tdingiz!",
                        "jwt": full_jwt({"user_id": new_user.id}),
                    }
                ),
                201,
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    except ValidationError as e:
        return jsonify({"error", e.errors()}), 400


@user_bp.route("/login", methods=["POST"])
async def login():
    data = request.json

    try:
        login = LoginSchema(**data)
        try:
            user = await User.get(username=login.username)
        except:
            return jsonify({"error": "Foydalanuvchi topilmadi"}), 404

        if not verify_password(login.password, user.password):
            return jsonify({"error": "Parol noto'g'ri"}), 401

        return jsonify(
            {
                "jwt": full_jwt({"user_id": user.id})
                # "message": f"Xush kelibsiz, {user.username}! Sizning ma'lumotlaringiz: Username - {user.username}, Email - {user.email}, Tizimga kirgan vaqt - {user.created_at}"
            }
        )
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400


@user_bp.route("/get", methods=["POST"])
async def get_user():
    data = request.json

    try:
        get = GetSchema(**data)

        current_user = await User.get(id=int(get.user_id))

        if current_user.is_superuser:
            target_user = await User.get(id=int(get.id))
            return jsonify(
                {
                    "id": target_user.id,
                    "username": target_user.username,
                    "email": target_user.email,
                }
            )
        else:
            return jsonify({"error": "Siz admin emassiz"}), 403
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
